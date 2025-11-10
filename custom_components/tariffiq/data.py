"""Custom types for tariffiq."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import TariffIQApiClient
    from .coordinator import TariffIQUpdateCoordinator


type TariffIQConfigEntry = ConfigEntry[TariffIQData]


@dataclass
class TariffIQData:
    """Data for the Blueprint integration."""

    client: TariffIQApiClient
    coordinator: TariffIQUpdateCoordinator
    integration: Integration
