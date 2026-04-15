from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([TowerOledText(hass.data[DOMAIN][entry.entry_id])], True)


class TowerOledText(CoordinatorEntity, TextEntity):
    _attr_name = "Tower OLED Text"
    _attr_has_entity_name = True
    _attr_unique_id = "tower_hardware_oled_text"
    _attr_native_max = 120
    _attr_mode = "text"

    @property
    def available(self):
        return self.coordinator.data["oled"]["available"]

    @property
    def native_value(self):
        return self.coordinator.data["oled"]["last_text"] or ""

    async def async_set_value(self, value: str) -> None:
        await self.coordinator.async_oled_text(value)
