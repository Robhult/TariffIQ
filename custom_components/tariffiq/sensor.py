"""TariffIQ sensor platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfEnergy,
)
from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.tariffiq.const import (
    CONF_DSO,
    CONF_DSO_MODEL,
    CONF_FUSE_SIZE,
    CONF_NAME,
    DOMAIN,
)

if TYPE_CHECKING:
    from datetime import datetime

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="peaks",
        translation_key="peaks",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
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
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the TariffIQ sensor."""
    async_add_entities(
        TariffIQSensor(hass, entity_description, entry)
        for entity_description in SENSORS
    )


class TariffIQSensor(SensorEntity):
    """TariffIQ Sensor class."""

    hass: HomeAssistant
    entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        description: SensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self.entry = entry

        data = entry.data

        self.entity_description = description
        self._attr_unique_id = f"{data[CONF_NAME]}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, data[CONF_NAME])},
            name=data[CONF_NAME],
            manufacturer=DOMAIN,
            model=f"{data[CONF_DSO]}_{data[CONF_DSO_MODEL]}_{data[CONF_FUSE_SIZE]}",
        )

    async def async_update(self) -> None:
        """Update the sensor state."""
        # Placeholder for update logic
        pass


class TariffIQPeakSensor(TariffIQSensor):
    """TariffIQ Peak Sensor class."""

    def __init__(
        self,
        hass: HomeAssistant,
        description: SensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the peak sensor."""
        super().__init__(hass, description, entry)

        self._last_updated: datetime | None = None
        self._attr_extra_state_attributes = {
            "peaks_dictionary": [],  # Placeholder for peaks dictionary, current month
            "peaks_history": [],  # Placeholder for peaks history, full
        }

    async def async_update(self) -> None:
        """Update the peak sensor state."""
        # Placeholder for peak update logic
        pass
