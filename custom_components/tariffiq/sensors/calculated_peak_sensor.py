"""TariffIQ Calculated Peak Sensor integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfEnergy,
)
from homeassistant.helpers.restore_state import RestoreEntity

from custom_components.tariffiq.sensors.sensorbase import SensorBase

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQCalculatedPeakSensor(SensorBase, RestoreEntity):
    """TariffIQ Calculated Peak Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.ENERGY
    state_class: SensorStateClass = SensorStateClass.MEASUREMENT
    native_unit_of_measurement: str = UnitOfEnergy.KILO_WATT_HOUR
    suggested_display_precision: int = 2
    icon: str = "mdi:chart-line"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
    ) -> None:
        """Initialize the predicted consumption sensor."""
        super().__init__(entry, coordinator, "Calculated Peak")

    @property
    def state(self) -> float:
        """Return the state of the peak sensor."""
        try:
            return round(self.coordinator.data.get("calculated_peak", 0.0), 2)
        except (TypeError, ValueError, AttributeError):
            return 0.0

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        ) and "calculated_peak" in self.coordinator.data
