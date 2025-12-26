"""TariffIQ data coordinator."""

from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.tariffiq.dso.dsobase import DSOBase

from .const import CONF_DSO_AND_MODEL, CONF_FUSE_SIZE
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
            update_interval=timedelta(minutes=15),
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

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the DSO."""
        try:
            LOGGER.debug("Fetching data from DSO instance")
            return {
                "tariff_active": self.dso_instance.tariff_active(),
                "fixed_cost": self.dso_instance.fixed_cost(),
                "fees": self.dso_instance.selected_fees,
                "currency": self.dso_instance.currency,
                "fuse_size": self.entry.data[CONF_FUSE_SIZE],
            }
        except Exception as error:
            LOGGER.error("Error fetching data from DSO: %s", error)
            raise
