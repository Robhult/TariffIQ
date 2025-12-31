"""TariffIQ sensor platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from custom_components.tariffiq.sensors.fixed_cost_sensor import TariffIQFixedCostSensor
from custom_components.tariffiq.sensors.peaks_sensor import TariffIQPeaksSensor
from custom_components.tariffiq.sensors.total_dso_cost_sensor import (
    TariffIQTotalDSOCostSensor,
)
from custom_components.tariffiq.sensors.variable_cost_sensor import (
    TariffIQVariableCostSensor,
)

from .const import (
    DOMAIN,
    TARIFF_OPTIONS,
)
from .coordinator import TariffIQDataCoordinator  # noqa: TC001
from .sensors.sensorbase import SensorBase  # noqa: TC001

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

COST_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="peaks_cost",
        translation_key="peaks_cost",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="fixed_cost",
        translation_key="fixed_cost",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="variable_cost",
        translation_key="variable_cost",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="current_tariff",
        translation_key="current_tariff",
        device_class=SensorDeviceClass.ENUM,
        options=TARIFF_OPTIONS,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the TariffIQ sensor."""
    coordinator: TariffIQDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorBase] = []

    entities.append(TariffIQPeaksSensor(hass, entry, coordinator))
    entities.append(TariffIQFixedCostSensor(hass, entry, coordinator))
    entities.append(TariffIQVariableCostSensor(hass, entry, coordinator))
    entities.append(TariffIQTotalDSOCostSensor(hass, entry, coordinator))

    async_add_entities(entities)
