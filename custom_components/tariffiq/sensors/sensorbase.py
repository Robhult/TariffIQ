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
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.tariffiq.const import (
    CONF_DSO_AND_MODEL,
    CONF_FUSE_SIZE,
    CONF_NAME,
    DOMAIN,
)
from custom_components.tariffiq.coordinator import TariffIQDataCoordinator
from custom_components.tariffiq.helpers import nametoid

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.device_registry import DeviceInfo

    from custom_components.tariffiq.dso.dsobase import DSOBase


class SensorBase(SensorEntity, CoordinatorEntity[TariffIQDataCoordinator]):
    """TariffIQ Base Sensor."""

    _entry: ConfigEntry
    _entry_id: str

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._attr_name = f"{entry.data[CONF_NAME]} {name}"

        super().__init__(coordinator)

    @property
    def dso_instance(self) -> DSOBase:
        """Return the DSO instance from coordinator."""
        return self.coordinator.dso_instance

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}_{self._entry.entry_id}_{nametoid(self._attr_name)}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.data[CONF_NAME],
            "manufacturer": "TariffIQ",
            "model": (
                f"{self._entry.data[CONF_DSO_AND_MODEL]}_{self._entry.data[CONF_FUSE_SIZE]}A"
            ),
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )
