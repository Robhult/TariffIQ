"""Statistics helper utilities for TariffIQ sensors."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.recorder.statistics import (
    StatisticsRow,
    statistics_during_period,
)
from homeassistant.helpers.recorder import get_instance
from homeassistant.util import dt as dt_util

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


class TariffIQStatisticsHelper:
    """Helper class for retrieving sensor statistics."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the statistics helper."""
        self.hass = hass
        self.recorder = get_instance(hass)

    async def get_hourly_stats(
        self,
        entity_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        types: set[str] | None = None,
    ) -> list[StatisticsRow]:
        """Fetch hourly statistics for any sensor."""
        if types is None:
            types = {"change"}

        return (
            await self.recorder.async_add_executor_job(
                statistics_during_period,
                self.hass,
                start_date,
                end_date,
                {entity_id},
                "hour",
                None,
                types,
            )
        ).get(entity_id, [])

    async def get_latest(self, entity_id: str, type: str | None = None) -> float:  # noqa: A002
        """Fetch statistics specifically for last change calculations."""
        if type is None:
            type = "state"  # noqa: A001

        stats = await self.get_hourly_stats(
            entity_id, dt_util.now() - timedelta(days=1), None, {type}
        )

        if len(stats) > 0:
            return stats.pop().get(type, 0.0) or 0.0

        return 0.0

    async def get_peak_stats(
        self,
        entity_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[StatisticsRow]:
        """Fetch statistics specifically for peak calculations."""
        return await self.get_hourly_stats(
            entity_id, start_date, end_date, {"max", "mean"}
        )

    async def get_consumption_stats(
        self,
        entity_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[StatisticsRow]:
        """Fetch statistics for consumption sensors."""
        return await self.get_hourly_stats(
            entity_id, start_date, end_date, {"sum", "change"}
        )
