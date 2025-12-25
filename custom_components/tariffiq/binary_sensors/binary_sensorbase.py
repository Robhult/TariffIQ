"""
Base class for TariffIQ binary sensors.

This module provides the BinarySensorBase class which serves as the foundation
for all TariffIQ binary sensors, handling tariff state detection and device
information setup.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity

from tariffiq.const import (
    CONF_DSO_AND_MODEL,
    CONF_FUSE_SIZE,
    CONF_NAME,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.device_registry import DeviceInfo


class BinarySensorBase(BinarySensorEntity):
    """TariffIQ Binary Sensor class."""

    hass: HomeAssistant
    entry: ConfigEntry
    key: str

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        key: str,
    ) -> None:
        """Initialize the binary sensor."""
        self.hass = hass
        self.entry = entry
        self.key = key

    @property
    def unique_id(self) -> str:
        """Return the unique ID."""
        return f"{self.entry.data[CONF_NAME]}_{self.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.entry.data[CONF_NAME])},
            "name": self.entry.data[CONF_NAME],
            "manufacturer": DOMAIN,
            "model": (
                f"{self.entry.data[CONF_DSO_AND_MODEL]}_{self.entry.data[CONF_FUSE_SIZE]}A"
            ),
        }
