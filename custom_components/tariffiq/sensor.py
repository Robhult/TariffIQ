"""TariffIQ sensor platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.tariffiq.sensors.cost_sensor import TariffIQCostSensor
from custom_components.tariffiq.sensors.peaks_sensor import TariffIQPeaksSensor
from custom_components.tariffiq.sensors.predicted_consumption_sensor import (
    TariffIQPredictedConsumptionSensor,
)

from .const import DOMAIN
from .coordinator import TariffIQDataCoordinator  # noqa: TC001
from .sensors.sensorbase import SensorBase  # noqa: TC001

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


cost_sensors = [
    ("Costs Peaks", "peaks_cost"),
    ("Costs Fixed", "fixed_cost"),
    ("Costs Variable", "variable_cost"),
    ("Costs Total DSO", "total_dso_cost"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the TariffIQ sensor."""
    coordinator: TariffIQDataCoordinator = hass.data[DOMAIN][config.entry_id]

    entities: list[SensorBase] = []

    entities.append(TariffIQPeaksSensor(config, coordinator))
    entities.append(TariffIQPredictedConsumptionSensor(config, coordinator))

    # Cost sensors
    for name, coordinator_key in cost_sensors:
        entities.append(TariffIQCostSensor(config, coordinator, name, coordinator_key))

    async_add_entities(entities)
