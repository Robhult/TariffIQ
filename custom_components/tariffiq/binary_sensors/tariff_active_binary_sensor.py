"""
Binary sensor for TariffIQ no tariff detection.

This module contains the TariffIQNoTariffBinarySensor class that provides
a binary sensor to indicate when no tariff information is available.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.tariffiq.binary_sensors.binary_sensorbase import BinarySensorBase

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQTariffActiveBinarySensor(BinarySensorBase):
    """Tariff active binary sensor."""

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
    ) -> None:
        """Initialize the Tariff Active binary sensor."""
        super().__init__(entry, coordinator, "Tariff Active")

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {
            "starts_at": self.coordinator.data.get("tariff_starts_at", "N/A"),
            "ends_at": self.coordinator.data.get("tariff_ends_at", "N/A"),
            "schedule": self.coordinator.data.get("tariff_schedule", "N/A"),
        }

    @property
    def is_on(self) -> bool:
        """Return true if tariff is active."""
        if not self.coordinator.data:
            return False
        return self.coordinator.data.get("tariff_active", False)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )
