"""TariffIQ Predicted Consumption Sensor integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    UnitOfEnergy,
)
from homeassistant.helpers.restore_state import RestoreEntity

from custom_components.tariffiq.sensors.sensorbase import SensorBase

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQPredictedConsumptionSensor(SensorBase, RestoreEntity):
    """TariffIQ Predicted Consumption Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.ENERGY
    native_unit_of_measurement: str = UnitOfEnergy.KILO_WATT_HOUR
    suggested_display_precision: int = 1
    icon: str = "mdi:chart-line"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
    ) -> None:
        """Initialize the predicted consumption sensor."""
        super().__init__(entry, coordinator, "Predicted Consumption")

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {
            "current_hour_consumption": self.coordinator.data.get(
                "current_hour_consumption_formatted", 0.0
            ),
        }

    @property
    def state(self) -> float:
        """Return the state of the peak sensor."""
        try:
            return round(self.coordinator.data.get("predicted_consumption", 0.0), 1)
        except (TypeError, ValueError, AttributeError):
            return 0.0

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        ) and "predicted_consumption" in self.coordinator.data
