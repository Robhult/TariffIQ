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

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQPeaksSensor(SensorBase, RestoreEntity):
    """TariffIQ Peaks Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.ENERGY
    unit_of_measurement: str = UnitOfEnergy.KILO_WATT_HOUR
    _sensor_option_display_precision: int = 2
    translation_key: str = "peaks"
    icon: str = "mdi:chart-line"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
    ) -> None:
        """Initialize the peak sensor."""
        self.name = "Peaks"

        super().__init__(hass, entry, coordinator, "peaks")

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {
            "current_hour_consumption": self.coordinator.data.get(
                "current_hour_consumption", 0.0
            ),
            "predicted_consumption": self.coordinator.data.get(
                "predicted_consumption", 0.0
            ),
            "peaks_dictionary": self.coordinator.data.get("peaks_dictionary", {}),
        }

    @property
    def state(self) -> float:
        """Return the state of the peak sensor."""
        return self.coordinator.data.get("peaks", 0.0)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )

    async def async_update(self) -> None:
        """Update the peak sensor state."""
