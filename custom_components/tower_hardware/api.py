from __future__ import annotations

import asyncio
import json
import shlex
from dataclasses import dataclass
from typing import Any

from .const import (
    CONF_LED_BINARY,
    CONF_OLED_BINARY,
    CONF_SSH_HOST,
    CONF_SSH_KEY_PATH,
    CONF_SSH_KNOWN_HOSTS,
    CONF_SSH_PORT,
    CONF_SSH_USER,
)


@dataclass
class TowerState:
    led_available: bool = False
    oled_available: bool = False
    led_is_on: bool = False
    led_r: int = 255
    led_g: int = 228
    led_b: int = 206
    led_brightness: int = 200
    led_effect: str | None = None
    oled_text: str = ""


class TowerApi:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.state = TowerState()

    def _ssh(self) -> list[str]:
        return [
            "ssh",
            "-i", self.data[CONF_SSH_KEY_PATH],
            "-o", "StrictHostKeyChecking=no",
            "-o", f"UserKnownHostsFile={self.data[CONF_SSH_KNOWN_HOSTS]}",
            "-p", str(self.data[CONF_SSH_PORT]),
            f"{self.data[CONF_SSH_USER]}@{self.data[CONF_SSH_HOST]}",
        ]

    async def _run(self, command: str) -> tuple[int, str, str]:
        proc = await asyncio.create_subprocess_exec(
            *self._ssh(),
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate()
        return proc.returncode, out.decode().strip(), err.decode().strip()

    async def _check_bin(self, path: str) -> bool:
        rc, _, _ = await self._run(f"test -x {shlex.quote(path)}")
        return rc == 0

    async def _must(self, cmd: str) -> str:
        rc, out, err = await self._run(cmd)
        if rc != 0:
            raise RuntimeError(err or out or f"command failed {rc}")
        return out

    async def probe(self) -> dict[str, Any]:
        self.state.led_available = await self._check_bin(self.data[CONF_LED_BINARY])
        self.state.oled_available = await self._check_bin(self.data[CONF_OLED_BINARY])

        if self.state.led_available:
            rc, out, _ = await self._run("cat /mnt/data/supervisor/share/tower_control/tower_led_state.json")
            if rc == 0 and out:
                try:
                    st = json.loads(out)
                    self.state.led_is_on = bool(st.get("is_on", False))
                    self.state.led_r = int(st.get("r", 255))
                    self.state.led_g = int(st.get("g", 228))
                    self.state.led_b = int(st.get("b", 206))
                    self.state.led_brightness = int(st.get("brightness", 200))
                    self.state.led_effect = st.get("effect") or None
                except Exception:
                    pass

        return {
            "led": {
                "available": self.state.led_available,
                "is_on": self.state.led_is_on,
                "r": self.state.led_r,
                "g": self.state.led_g,
                "b": self.state.led_b,
                "brightness": self.state.led_brightness,
                "effect": self.state.led_effect,
            },
            "oled": {
                "available": self.state.oled_available,
                "last_text": self.state.oled_text,
            },
        }

    async def led_off(self):
        await self._must(f"{self.data[CONF_LED_BINARY]} off")

    async def led_color(self, r: int, g: int, b: int, brightness: int):
        await self._must(f"{self.data[CONF_LED_BINARY]} color {r} {g} {b} {brightness}")

    async def led_effect(self, name: str):
        mapping = {
            "Blink Slow": "blink_slow",
            "Blink Fast": "blink_fast",
            "Rainbow": "rainbow",
            "Pulse": "pulse",
        }
        await self._must(f"{self.data[CONF_LED_BINARY]} effect {mapping[name]}")

    async def oled_text(self, text: str):
        lines = [line.rstrip() for line in text.splitlines()]
        lines = [l for l in lines if l != ""]
        if not lines:
            lines = [""]
        if len(lines) == 1:
            await self._must(f"{self.data[CONF_OLED_BINARY]} text {shlex.quote(lines[0][:20])}")
        elif len(lines) == 2:
            await self._must(
                f"{self.data[CONF_OLED_BINARY]} text2 "
                f"{shlex.quote(lines[0][:20])} {shlex.quote(lines[1][:20])}"
            )
        else:
            await self._must(
                f"{self.data[CONF_OLED_BINARY]} text3 "
                f"{shlex.quote(lines[0][:20])} "
                f"{shlex.quote(lines[1][:20])} "
                f"{shlex.quote(lines[2][:20])}"
            )
        self.state.oled_text = "\n".join(lines[:3])
