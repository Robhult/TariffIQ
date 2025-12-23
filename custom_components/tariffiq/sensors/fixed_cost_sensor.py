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


class TariffIQFixedCostSensor(SensorBase, RestoreEntity):
    """TariffIQ Fixed Cost Sensor class."""

    device_class: SensorDeviceClass = SensorDeviceClass.MONETARY
    state_class: str = SensorStateClass.TOTAL
    icon: str = "mdi:money"
    name: str = "Fixed Cost"
    translation_key: str = "fixed_cost"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        key: str,
    ) -> None:
        """Initialize the peak sensor."""
        super().__init__(hass, entry, key)
