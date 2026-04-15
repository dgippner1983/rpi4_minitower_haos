# Tower Control for Home Assistant 0.0.1

## 🇬🇧 English

This repository provides a complete package for using the Raspberry Pi 4 [Waveshare PI4B Mini Tower Acce](https://www.waveshare.com/wiki/PI4B_Mini_Tower_Acce#Connection_Details) with Home Assistant:

- **Home Assistant Add-on** to deploy native host control binaries (`tower_ledctl`, `tower_oledctl`)
- **Custom Integration** (`tower_hardware`) for direct LED/OLED control in Home Assistant
- **HACS-compatible layout** so the integration can be installed from a custom repository

### Included components

- Add-on: `addons/tower_control`
- Integration (HACS/custom component): `custom_components/tower_hardware`
- Existing source/development structure: `Addon/` and `Integration/`

### Features

- LED exposed as a `light` entity (`Tower LED`) with color, brightness, and effects
- OLED exposed as a `text` entity (`Tower OLED Text`) with up to 3 lines
- LED/OLED availability as `binary_sensor` entities
- Configurable SSH execution for host-side binaries

### Add-on installation (Home Assistant Add-on Repository)

1. Host this repository on GitHub.
2. In Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories**.
3. Add your repository URL.
4. Install and start the **Tower Control** add-on.

### Integration installation via HACS

1. In HACS: **Integrations → ⋮ → Custom repositories**.
2. Add the repository URL and choose category **Integration**.
3. Install **Tower Hardware**.
4. Restart Home Assistant.
5. Add the integration via **Settings → Devices & Services**.

Default integration binary paths:

- LED: `/mnt/data/supervisor/share/tower_control/tower_ledctl`
- OLED: `/mnt/data/supervisor/share/tower_control/tower_oledctl`

## Documentation

A short feature documentation is available in `documentation/functions.md`.

---

## 🇩🇪 Deutsch

Dieses Repository enthält ein vollständiges Paket für den Raspberry Pi 4 [Waveshare PI4B Mini Tower Acce](https://www.waveshare.com/wiki/PI4B_Mini_Tower_Acce#Connection_Details) in Home Assistant:

- **Home Assistant Add-on** zum Bereitstellen der nativen Steuerungs-Binaries auf dem Host (`tower_ledctl`, `tower_oledctl`)
- **Custom Integration** (`tower_hardware`) zur direkten Einbindung von LED- und OLED-Steuerung in Home Assistant
- **HACS-kompatible Struktur**, damit die Integration als Custom Repository installiert werden kann

### Enthaltene Bestandteile

- Add-on: `addons/tower_control`
- Integration (HACS/Custom Component): `custom_components/tower_hardware`
- Zusätzliche Entwickler-/Quellstruktur (bestehend): `Addon/` und `Integration/`

### Funktionsumfang

- LED als `light`-Entity (`Tower LED`) mit Farbe, Helligkeit und Effekten
- OLED als `text`-Entity (`Tower OLED Text`) mit bis zu 3 Zeilen
- Verfügbarkeits-Sensoren für LED/OLED als `binary_sensor`
- Konfigurierbare SSH-Verbindung zur Ausführung der Host-Binaries

### Installation Add-on (Home Assistant Add-on Repository)

1. Dieses Repository in GitHub bereitstellen.
2. In Home Assistant: **Einstellungen → Add-ons → Add-on-Store → ⋮ → Repositories**.
3. Repository-URL eintragen.
4. Add-on **Tower Control** installieren und starten.

### Installation Integration über HACS

1. In HACS: **Integrationen → ⋮ → Benutzerdefinierte Repositories**.
2. Repository-URL eintragen und Kategorie **Integration** auswählen.
3. **Tower Hardware** installieren.
4. Home Assistant neu starten.
5. Integration über **Einstellungen → Geräte & Dienste** hinzufügen.

Standardpfade in der Integration:

- LED: `/mnt/data/supervisor/share/tower_control/tower_ledctl`
- OLED: `/mnt/data/supervisor/share/tower_control/tower_oledctl`
