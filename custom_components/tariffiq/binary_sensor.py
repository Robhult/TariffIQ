"""TariffIQ binary sensor platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import CONF_DSO, CONF_DSO_MODEL, CONF_FUSE_SIZE, CONF_NAME, DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="no_tariff",
        translation_key="no_tariff",
    ),
    BinarySensorEntityDescription(
        key="low_tariff",
        translation_key="low_tariff",
    ),
    BinarySensorEntityDescription(
        key="high_tariff",
        translation_key="high_tariff",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the TariffIQ binary sensor."""
    async_add_entities(
        TariffIQBinarySensor(hass, entity_description, entry)
        for entity_description in BINARY_SENSORS
    )


class TariffIQBinarySensor(BinarySensorEntity):
    """TariffIQ Binary Sensor class."""

    hass: HomeAssistant
    entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        description: BinarySensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        self.hass = hass
        self.entry = entry

        data = entry.data

        self.entity_description = description
        self._attr_unique_id = f"{data[CONF_NAME]}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, data[CONF_NAME])},
            name=data[CONF_NAME],
            manufacturer=DOMAIN,
            model=f"{data[CONF_DSO]}_{data[CONF_DSO_MODEL]}_{data[CONF_FUSE_SIZE]}",
        )
