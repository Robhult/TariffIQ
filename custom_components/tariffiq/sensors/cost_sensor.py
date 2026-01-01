"""TariffIQ Cost Sensor integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

from custom_components.tariffiq.sensors.sensorbase import SensorBase

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQCostSensor(SensorBase):
    """TariffIQ Cost Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.MONETARY
    state_class: str = SensorStateClass.TOTAL
    suggested_display_precision: int = 2
    icon: str = "mdi:cash"

    _coordinator_key: str

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
        name: str,
        coordinator_key: str,
    ) -> None:
        """Initialize the cost sensor."""
        self._coordinator_key = coordinator_key

        super().__init__(entry, coordinator, name)

    @property
    def native_value(self) -> float | None:
        """Return state."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self._coordinator_key, 0.0)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement (currency) from DSO."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("currency")

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )
