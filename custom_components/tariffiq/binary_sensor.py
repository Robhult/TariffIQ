"""TariffIQ binary sensor platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.tariffiq.binary_sensors.tariff_active_binary_sensor import (
    TariffIQTariffActiveBinarySensor,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.tariffiq.binary_sensors.binary_sensorbase import (
        BinarySensorBase,
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the TariffIQ binary sensor."""
    entities: list[BinarySensorBase] = []

    entities.append(TariffIQTariffActiveBinarySensor(hass, entry))

    async_add_entities(entities)
