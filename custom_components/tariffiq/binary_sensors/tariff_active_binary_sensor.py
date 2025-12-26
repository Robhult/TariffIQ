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
    from homeassistant.core import HomeAssistant

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQTariffActiveBinarySensor(BinarySensorBase):
    """Tariff active binary sensor."""

    translation_key: str = "tariff_active"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
    ) -> None:
        """Initialize the Tariff Active binary sensor."""
        self.name = "Tariff Active"

        super().__init__(
            hass,
            entry,
            coordinator,
            key="tariff_active",
        )

    @property
    def is_on(self) -> bool:
        """Return true if tariff is active."""
        return self.coordinator.dso_instance.tariff_active()
