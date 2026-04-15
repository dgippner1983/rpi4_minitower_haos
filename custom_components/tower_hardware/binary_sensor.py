from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LedAvailable(c), OledAvailable(c)], True)


class _B(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)


class LedAvailable(_B):
    _attr_name = "Tower LED Available"
    _attr_has_entity_name = True
    _attr_unique_id = "tower_led_available"

    @property
    def is_on(self):
        return self.coordinator.data["led"]["available"]


class OledAvailable(_B):
    _attr_name = "Tower OLED Available"
    _attr_has_entity_name = True
    _attr_unique_id = "tower_oled_available"

    @property
    def is_on(self):
        return self.coordinator.data["oled"]["available"]
