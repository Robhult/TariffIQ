"""TariffIQ data coordinator."""

from datetime import timedelta
from typing import Any

from homeassistant.components.recorder.statistics import (
    statistics_during_period,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.recorder import get_instance
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from custom_components.tariffiq.dso.dsobase import DSOBase

from .const import (
    CONF_DSO_AND_MODEL,
    CONF_ENERGY_SENSOR,
    CONF_FUSE_SIZE,
    CONF_POWER_SENSOR,
)
from .dso import get_dso_class
from .helpers import LOGGER


class TariffIQDataCoordinator(DataUpdateCoordinator):
    """TariffIQ Data Coordinator to manage data updates."""

    entry: ConfigEntry
    dso_instance: DSOBase

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name="TariffIQ",
            update_interval=timedelta(minutes=5),
        )
        self.entry = entry

        try:
            # Initialize DSO class instance
            dso_class = get_dso_class(self.entry.data[CONF_DSO_AND_MODEL])
            LOGGER.debug(
                "Initializing DSO class %s with fuse size %s",
                dso_class.__name__,
                self.entry.data[CONF_FUSE_SIZE],
            )
            self.dso_instance = dso_class(self.entry.data[CONF_FUSE_SIZE])
        except Exception as error:
            LOGGER.error("Error initializing DSO instance: %s", error)
            raise

    def _get_energy_sensor_value(self) -> float:
        """Fetch and validate energy sensor value."""
        energy_sensor_entity_id = self.entry.data[CONF_ENERGY_SENSOR]
        energy_sensor_state = self.hass.states.get(energy_sensor_entity_id)

        if energy_sensor_state and energy_sensor_state.state not in [
            "unavailable",
            "unknown",
            "none",
        ]:
            try:
                return float(energy_sensor_state.state)
            except (ValueError, TypeError):
                LOGGER.warning(
                    "Could not convert energy sensor state to float: %s",
                    energy_sensor_state.state,
                )
                return 0.0
        else:
            LOGGER.warning(
                "Energy sensor not available or invalid: %s",
                energy_sensor_entity_id,
            )
            return 0.0

    def _get_power_sensor_value(self) -> int:
        """Fetch and validate power sensor value."""
        power_sensor_entity_id = self.entry.data[CONF_POWER_SENSOR]
        power_sensor_state = self.hass.states.get(power_sensor_entity_id)

        if power_sensor_state and power_sensor_state.state not in [
            "unavailable",
            "unknown",
            "none",
        ]:
            try:
                return int(power_sensor_state.state)
            except (ValueError, TypeError):
                LOGGER.warning(
                    "Could not convert power sensor state to int: %s",
                    power_sensor_state.state,
                )
                return 0
        else:
            LOGGER.warning(
                "Power sensor not available or invalid: %s",
                power_sensor_entity_id,
            )
            return 0

    async def _get_current_hour_consumption(self) -> float:
        # Fetch current hour consumption from recorder statistics
        recorder_instance = get_instance(self.hass)
        stats = (
            await recorder_instance.async_add_executor_job(
                statistics_during_period,
                self.hass,
                dt_util.now() - timedelta(hours=2),
                None,
                {self.entry.data[CONF_ENERGY_SENSOR]},
                "hour",
                None,
                {"state"},
            )
        ).get(self.entry.data[CONF_ENERGY_SENSOR], [])

        LOGGER.debug("Fetched statistics: %s", stats)

        stats_value = stats.pop().get("state", 0.0) if stats else 0.0
        return self._get_energy_sensor_value() - (stats_value or 0.0)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the DSO."""
        try:
            LOGGER.debug("Fetching data from DSO instance")

            # Fetch energy sensor value
            energy_value = self._get_energy_sensor_value()
            power_value = self._get_power_sensor_value()

            current_hour_consumption = await self._get_current_hour_consumption()
            expected_peak = (
                current_hour_consumption + power_value / 1000
                if self.dso_instance.tariff_active()
                else 0.0
            )

            fixed_cost = self.dso_instance.fixed_cost()
            variable_cost = self.dso_instance.variable_cost(energy_value)
            peaks_cost = 0.0  # TODO: Placeholder for peaks cost calculation
            total_dso_cost = fixed_cost + variable_cost + peaks_cost

            data = {
                # Tariff Active Binary Sensor
                "tariff_active": self.dso_instance.tariff_active(),
                "tariff_starts_at": self.dso_instance.tariff_starts_at(),
                "tariff_ends_at": self.dso_instance.tariff_ends_at(),
                "tariff_schedule": self.dso_instance.tariff_schedule,
                # Peaks Sensor
                "peaks": 0.0,  # Placeholder for peaks value
                "current_hour_consumption": current_hour_consumption,
                "expected_peak": expected_peak,
                # DSO Cost Sensors
                "fixed_cost": fixed_cost,
                "variable_cost": variable_cost,
                "peaks_cost": 0.0,  # Placeholder for peaks cost value
                "total_dso_cost": total_dso_cost,
                # Consumption tracking data
                "energy_value": energy_value,  # Current energy reading
                "power_value": power_value,  # Current power reading
                # Misc States
                "fees": self.dso_instance.selected_fees,
                "currency": self.dso_instance.currency,
                "fuse_size": self.entry.data[CONF_FUSE_SIZE],
            }
            LOGGER.debug("Fetched data: %s", data)
        except Exception as error:
            LOGGER.error("Error fetching data from DSO: %s", error)
            raise
        else:
            return data
