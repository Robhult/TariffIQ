"""
Custom integration TariffIQ for Home Assistant.

For more details about this integration, please refer to
https://github.com/robhult/tariffiq
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, Platform
from homeassistant.core import HomeAssistant

from custom_components.tariffiq.coordinator import TariffIQDataCoordinator

from .const import DATA_HASS_CONFIG, DOMAIN
from .services import async_setup_services

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.typing import ConfigType

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the TariffIQ component."""
    hass.data[DATA_HASS_CONFIG] = config

    async_setup_services(hass)

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> bool:
    """Set up TariffIQ."""
    # Check if Home Assistant has already started
    if hass.is_running:
        # HA already started, setup coordinator immediately
        await _setup_coordinator(hass, config_entry)
    else:
        # Wait for HA to fully start before setting up coordinator
        async def setup_on_start(_event: object) -> None:
            """Set up coordinator when HA starts."""
            await _setup_coordinator(hass, config_entry)

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, setup_on_start)

    return True


async def _setup_coordinator(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Set up the coordinator and platforms."""
    # Create coordinator
    coordinator = TariffIQDataCoordinator(hass, config_entry)

    # Fetch initial data using the newer method
    await coordinator.async_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)


async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok
