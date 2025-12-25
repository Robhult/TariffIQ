"""
Base sensor class for TariffIQ integration.

This module provides the SensorBase class which serves as the foundation
for all TariffIQ sensors, handling common functionality like device info
and unique ID generation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
)

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


class SensorBase(SensorEntity):
    """TariffIQ Base Sensor."""

    hass: HomeAssistant
    entry: ConfigEntry
    key: str

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        key: str,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self.entry = entry
        self.key = key

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the binary sensor."""
        conf_name: str = self.entry.data[CONF_NAME].replace("TariffIQ", "")
        return f"{conf_name}_{self.key}".lower()

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
