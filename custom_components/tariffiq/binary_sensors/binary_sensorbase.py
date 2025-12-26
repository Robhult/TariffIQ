"""
Base class for TariffIQ binary sensors.

This module provides the BinarySensorBase class which serves as the foundation
for all TariffIQ binary sensors, handling tariff state detection and device
information setup.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.tariffiq.coordinator import TariffIQDataCoordinator
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

    from custom_components.tariffiq.dso.dsobase import DSOBase


class BinarySensorBase(CoordinatorEntity[TariffIQDataCoordinator], BinarySensorEntity):
    """TariffIQ Binary Sensor class."""

    hass: HomeAssistant
    entry: ConfigEntry
    key: str

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
        key: str,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.hass = hass
        self.entry = entry
        self.key = key

    @property
    def dso_instance(self) -> DSOBase:
        """Return the DSO instance from coordinator."""
        return self.coordinator.dso_instance

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

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )
