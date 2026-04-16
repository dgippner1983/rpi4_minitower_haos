# Tower Control for Home Assistant 0.0.3

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

### SSH key setup

The integration connects to the HA host via SSH to execute the control binaries. Key-based authentication is required.

> **No SSH host access yet?** SSH access to the underlying HAOS host (port 22222) is not enabled by default. You can set it up using the community add-on [HassOS SSH Port 22222 Configurator](https://community.home-assistant.io/t/add-on-hassos-ssh-port-22222-configurator/264109).

**1. Generate a key pair** (run in the HA terminal or SSH add-on):

```bash
mkdir -p /config/.ssh
ssh-keygen -t ed25519 -f /config/.ssh/id_ed25519 -N ""
```

**2. Authorize the key on the host:**

```bash
ssh-copy-id -i /config/.ssh/id_ed25519.pub -p 22222 root@127.0.0.1
```

Or manually append the contents of `/config/.ssh/id_ed25519.pub` to `/root/.ssh/authorized_keys` on the host.

**3. Test the connection:**

```bash
ssh -i /config/.ssh/id_ed25519 -p 22222 root@127.0.0.1 "echo ok"
```

The integration uses the private key at `/config/.ssh/id_ed25519` by default. This path can be changed during integration setup.

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

### SSH-Schlüssel einrichten

Die Integration verbindet sich per SSH mit dem HA-Host, um die Steuerungs-Binaries auszuführen. Es wird eine schlüsselbasierte Authentifizierung benötigt.

> **Noch kein SSH-Host-Zugriff?** Der SSH-Zugriff auf den HAOS-Host (Port 22222) ist standardmäßig nicht aktiviert. Er kann mit dem Community-Add-on [HassOS SSH Port 22222 Configurator](https://community.home-assistant.io/t/add-on-hassos-ssh-port-22222-configurator/264109) eingerichtet werden.

**1. Schlüsselpaar generieren** (im HA-Terminal oder SSH-Add-on ausführen):

```bash
mkdir -p /config/.ssh
ssh-keygen -t ed25519 -f /config/.ssh/id_ed25519 -N ""
```

**2. Öffentlichen Schlüssel auf dem Host autorisieren:**

```bash
ssh-copy-id -i /config/.ssh/id_ed25519.pub -p 22222 root@127.0.0.1
```

Alternativ den Inhalt von `/config/.ssh/id_ed25519.pub` manuell an `/root/.ssh/authorized_keys` auf dem Host anhängen.

**3. Verbindung testen:**

```bash
ssh -i /config/.ssh/id_ed25519 -p 22222 root@127.0.0.1 "echo ok"
```

Die Integration verwendet standardmäßig den privaten Schlüssel unter `/config/.ssh/id_ed25519`. Der Pfad kann bei der Einrichtung der Integration angepasst werden.
