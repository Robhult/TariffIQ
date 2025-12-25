"""
Binary sensor for TariffIQ no tariff detection.

This module contains the TariffIQNoTariffBinarySensor class that provides
a binary sensor to indicate when no tariff information is available.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.tariffiq.binary_sensors.binary_sensorbase import BinarySensorBase
from custom_components.tariffiq.dso import get_dso_class
from tariffiq.const import (
    CONF_DSO_AND_MODEL,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


class TariffIQTariffActiveBinarySensor(BinarySensorBase):
    """Tariff active binary sensor."""

    translation_key: str = "tariff_active"
    name: str = "Tariff Active"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Tariff Active binary sensor."""
        super().__init__(
            hass,
            entry,
            key="tariff_active",
        )

    @property
    def is_on(self) -> bool:
        """Return true if tariff is active."""
        return get_dso_class(self.entry.data[CONF_DSO_AND_MODEL]).tariff_active()
