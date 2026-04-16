# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tower Control for Home Assistant — hardware integration for the Waveshare PI4B Mini Tower accessory (WS2812 LED strip + SSD1306 OLED display) on a Raspberry Pi 4 running Home Assistant OS (HAOS).

Two components:
- **Add-on** (`addons/tower_control/`): Builds native C binaries via Docker and deploys them to the HA host.
- **Custom Integration** (`custom_components/tower_hardware/`): Python HA integration that controls hardware remotely over SSH.

## Build & Deployment

### Add-on (C binaries)

There is no local build command — compilation happens inside Docker when the add-on is built by Home Assistant. The Dockerfile performs a multi-stage build:
1. Installs `build-base`, `linux-headers`, `python3`, `pillow`, `freetype`, `scons`
2. Clones Overpass-SemiBold font and generates `overpass_font.h` via `gen_overpass_font.py`
3. Compiles `tower_oledctl.c` (statically linked)
4. Clones and builds `rpi_ws281x` as a static library, then compiles `tower_ledctl.c`

Target architectures: `aarch64`, `armv7`, `armhf`

To test the add-on build locally (requires Docker):
```bash
docker build --build-arg BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest addons/tower_control/
```

### Integration (Python)

No test suite or linter is configured. The integration is loaded by Home Assistant directly from `custom_components/tower_hardware/`.

## Architecture

### Data Flow

```
HA UI / automations
    ↓
config_flow.py          — one-time setup of SSH credentials and binary paths
    ↓
coordinator.py          — DataUpdateCoordinator, 20s polling interval
    ↓
api.py (TowerApi)       — asyncio subprocess SSH calls to HA host
    ↓
Host binaries (SSH)
    ├── tower_ledctl    — WS2812 LED control (GPIO 21, DMA 10)
    └── tower_oledctl   — I2C SSD1306 OLED (address 0x3C, 128×64px)
```

### Integration Internals (`custom_components/tower_hardware/`)

- **`api.py`**: All SSH communication. `TowerApi.probe()` checks binary availability and reads LED state from a JSON file on the host. Commands call the binaries with CLI arguments. State is persisted on the host at `/mnt/data/supervisor/share/tower_control/tower_led_state.json`.
- **`coordinator.py`**: Wraps `TowerApi`. Each command method (`async_led_off`, `async_led_color`, `async_led_effect`, `async_oled_text`) executes via the API, then calls `async_refresh()` to propagate new state to entities.
- **`light.py`**: `TowerLedLight` — RGB color mode with brightness, effects: `Blink Slow`, `Blink Fast`, `Rainbow`, `Pulse`.
- **`text.py`**: `TowerOledText` — max 120 chars, split across up to 3 lines of 20 chars.
- **`binary_sensor.py`**: `LedAvailable` / `OledAvailable` — reflect whether each binary exists on the host.

### Add-on Internals (`addons/tower_control/`)

- **`tower_ledctl.c`**: Drives WS2812 via `rpi_ws281x`. Effects fork a child process; the PID is written to a file so subsequent calls can kill the previous effect. State is written as JSON after every command.
- **`tower_oledctl.c`**: Drives SSD1306 over I2C using raw `ioctl`. Font glyphs are embedded from the generated `overpass_font.h`. Supports `text`, `text2`, `text3` subcommands for 1–3 line display.
- **`run.sh`**: Copies compiled binaries from the add-on directory to `/share/tower_control/`, then starts the LED and OLED daemons.

### Key Defaults (from `const.py`)

| Setting | Default |
|---|---|
| `ssh_host` | `127.0.0.1` |
| `ssh_port` | `22222` |
| `ssh_user` | `root` |
| `ssh_key_path` | `/config/.ssh/id_ed25519` |
| `led_binary` | `/mnt/data/supervisor/share/tower_control/tower_ledctl` |
| `oled_binary` | `/mnt/data/supervisor/share/tower_control/tower_oledctl` |

## Important Constraints

- The add-on requires **`SYS_RAWIO` privilege** and access to `/dev/mem` for WS2812 GPIO control via DMA.
- SSH uses **key-based auth only** — no password auth.
- The integration runs inside the HA container and reaches the host via SSH on port 22222 (HA OS exposes this).
- All user-facing strings must be added to both `en` and `de` sections of `strings.json`.
- HACS compatibility requires keeping `hacs.json` and `repository.yaml` in sync with `manifest.json` versions.
