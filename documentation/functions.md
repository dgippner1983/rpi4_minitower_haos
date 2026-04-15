# Tower Control – Funktionsdokumentation / Feature Documentation

## 🇩🇪 Deutsch

### Add-on `tower_control`

Das Add-on baut/bereitstellt die nativen Host-Tools und startet sie mit den konfigurierten Optionen.

**Wichtige Dateien:**
- `addons/tower_control/config.yaml`: Add-on-Metadaten, Optionen und Schema
- `addons/tower_control/run.sh`: Startlogik und Übergabe der Optionen
- `addons/tower_control/tower_ledctl.c`: LED-Steuerung inkl. Effekte
- `addons/tower_control/tower_oledctl.c`: OLED-Textausgabe

### Integration `tower_hardware`

Die Integration verbindet Home Assistant per SSH mit dem Host und steuert die Binaries.

**Konfiguration (Config Flow):**
- SSH-Host, Port, Nutzer
- SSH-Key-Pfad und known_hosts
- Pfad zu LED- und OLED-Binary

**Entitäten:**
- `light.Tower LED`
  - Farbe (RGB)
  - Helligkeit
  - Effekte: Blink Slow, Blink Fast, Rainbow, Pulse
- `text.Tower OLED Text`
  - Übergibt 1–3 Textzeilen (je max. 20 Zeichen)
- `binary_sensor.Tower LED Available`
- `binary_sensor.Tower OLED Available`

**Ablauf:**
1. Coordinator pollt zyklisch den Zustand.
2. API prüft Verfügbarkeit der Binaries (`test -x ...`).
3. Befehle werden per SSH remote ausgeführt.
4. State-Änderungen werden in Home Assistant aktualisiert.

## 🇬🇧 English

### Add-on `tower_control`

The add-on builds/deploys native host tools and starts them with configured options.

**Key files:**
- `addons/tower_control/config.yaml`: add-on metadata, options, schema
- `addons/tower_control/run.sh`: startup logic and option mapping
- `addons/tower_control/tower_ledctl.c`: LED control incl. effects
- `addons/tower_control/tower_oledctl.c`: OLED text output

### Integration `tower_hardware`

The integration connects Home Assistant to host binaries via SSH.

**Configuration (Config Flow):**
- SSH host, port, user
- SSH key path and known_hosts
- LED and OLED binary paths

**Entities:**
- `light.Tower LED`
  - RGB color
  - brightness
  - effects: Blink Slow, Blink Fast, Rainbow, Pulse
- `text.Tower OLED Text`
  - sends 1–3 text lines (max. 20 chars each)
- `binary_sensor.Tower LED Available`
- `binary_sensor.Tower OLED Available`

**Flow:**
1. Coordinator polls state periodically.
2. API checks binary availability (`test -x ...`).
3. Commands are executed remotely over SSH.
4. Entity states are refreshed in Home Assistant.
