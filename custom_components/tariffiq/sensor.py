"""TariffIQ sensor platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from custom_components.tariffiq.sensors.peak_sensor import TariffIQPeakSensor

from .const import (
    TARIFF_OPTIONS,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.tariffiq.sensors.sensorbase import SensorBase

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
    entities: list[SensorBase] = []

    entities.append(TariffIQPeakSensor(hass, entry))

    async_add_entities(entities)
