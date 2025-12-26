"""TariffIQ Fixed Cost Sensor integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.restore_state import RestoreEntity

from custom_components.tariffiq.sensors.sensorbase import SensorBase

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from custom_components.tariffiq.coordinator import TariffIQDataCoordinator


class TariffIQFixedCostSensor(SensorBase, RestoreEntity):
    """TariffIQ Fixed Cost Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.MONETARY
    state_class: str = SensorStateClass.TOTAL
    _attr_suggested_display_precision: int = 2
    icon: str = "mdi:cash"
    translation_key: str = "fixed_cost"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: TariffIQDataCoordinator,
    ) -> None:
        """Initialize the fixed cost sensor."""
        self.name = "Fixed Cost"

        super().__init__(hass, entry, coordinator, "fixed_cost")

    @property
    def native_value(self) -> float | None:
        """Return the fixed cost value."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("fixed_cost")

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
