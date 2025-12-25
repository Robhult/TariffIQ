"""TariffIQ Peaks Sensor integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
)
from homeassistant.const import (
    UnitOfEnergy,
)
from homeassistant.helpers.restore_state import RestoreEntity

from custom_components.tariffiq.sensors.sensorbase import SensorBase

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


class TariffIQPeaksSensor(SensorBase, RestoreEntity):
    """TariffIQ Peaks Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.ENERGY
    unit_of_measurement: str = UnitOfEnergy.KILO_WATT_HOUR
    translation_key: str = "peaks"
    icon: str = "mdi:chart-line"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the peak sensor."""
        self.name = "Peaks"

        super().__init__(hass, entry, "peaks")

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {
            "expected_peak": 0.0,  # Placeholder for expected peak value
            "peaks_dictionary": {
                "17h12": 0.1,
                "12h13": 0.2,
                "06h14": 0.3,
            },  # Placeholder for peaks dictionary. Current month
            "peaks_history": {
                "2025-12": [0.1, 0.2, 0.3],
                "2025-11": [0.1, 0.2, 0.3],
            },  # Placeholder for peaks history. 12 months back
        }

    @property
    def state(self) -> float:
        """Return the state of the peak sensor."""
        return 0.0

    async def async_update(self) -> None:
        """Update the peak sensor state."""
        pass
