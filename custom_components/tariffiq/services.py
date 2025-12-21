"""Services for the TariffIQ component."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, callback


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the TariffIQ component."""
