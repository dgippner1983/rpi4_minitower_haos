Tower Control V3.1

Enthalten:
- Add-on: addons/tower_control_builder
  Deployt Host-Tools nach /share/tower_control
  * tower_ledctl   (LED mit Effekten)
  * tower_oledctl  (OLED, Overpass SemiBold)
- Custom Integration: custom_components/tower_hardware
  * light.tower_led
  * text.tower_oled_text
  * fan.tower_fan (pigpio-basiert via shell_command/HA-Service im Package)
  * binary_sensor.tower_led_available
  * binary_sensor.tower_oled_available
- Package: packages/tower_control.yaml
  * stabile OLED-Rotation
  * temperaturabhängige Lüfterregelung
  * pigpio shell_command für GPIO14 PWM

Wichtige Architektur:
- LED und OLED laufen nativ über die Tower-Integration und Host-Binaries.
- Fan bleibt bewusst pigpio-basiert, weil das bei dir schon stabil ist.
  Die fan-Entity ist deshalb in V3.1 noch nicht nativ in der Integration, sondern
  die Regelung läuft sauber über shell_command + pigpio.
  Das vermeidet Konflikte mit deiner stabilen pigpio-Basis.

Installation:
1. ZIP nach /config entpacken.
2. configuration.yaml:
   homeassistant:
     packages: !include_dir_named packages
3. Lokales Add-on "Tower Control Builder" bauen und einmal starten.
4. Home Assistant neu starten.
5. Integration "Tower Hardware" hinzufügen.
   Standardpfade:
   - LED:  /mnt/data/supervisor/share/tower_control/tower_ledctl
   - OLED: /mnt/data/supervisor/share/tower_control/tower_oledctl

LED-Effekte in light.tower_led:
- Blink Slow
- Blink Fast
- Rainbow
- Pulse
