"""Base model classes for DSO (Distribution System Operator) pricing models."""

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import ClassVar

from homeassistant.components.recorder.statistics import StatisticsRow

from custom_components.tariffiq.const import LOGGER, NOTIMPLEMENTED_MSG
from custom_components.tariffiq.dso.helpers.tariff_schedule import TariffSchedule


class ModelBase(ABC):
    """Base class for DSO pricing models."""

    tariff_schedule: ClassVar[TariffSchedule]

    @classmethod
    @abstractmethod
    def peak_value(cls, statistics: dict[str, list[StatisticsRow]]) -> float:
        """Return the peak value for the model."""
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    @classmethod
    @abstractmethod
    def observed_peak(
        cls, statistics: dict[str, list[StatisticsRow]]
    ) -> list[dict[str, float]]:
        """Return the peak values for the model."""
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    @classmethod
    def _filter_statistics(
        cls,
        statistics: list[StatisticsRow],
        months: set[int] | None = None,
        weekdays: set[int] | None = None,
        hours: set[int] | None = None,
    ) -> list[StatisticsRow]:
        """
        Filter statistics by months, days of week, and hours.

        Args:
            statistics: List of StatisticsRow objects
            months: Set of months (1-12) to include, None for all
            weekdays: Set of weekdays (0=Monday, 6=Sunday) to include, None for all
            hours: Set of hours (0-23) to include, None for all

        Returns:
            Filtered list of StatisticsRow objects

        """
        filtered = []

        for stat in statistics:
            start_time = datetime.fromtimestamp(stat.get("start", 0.0))  # noqa: DTZ006
            if start_time is None or not isinstance(start_time, (datetime, date)):
                LOGGER.debug("Skipping statistic with invalid start time: %s", stat)
                continue

            # Check month filter
            if months is not None and start_time.month not in months:
                continue

            # Check weekday filter (0=Monday, 6=Sunday)
            if weekdays is not None and start_time.weekday() not in weekdays:
                continue

            # Check hour filter
            if hours is not None and start_time.hour not in hours:
                continue

            filtered.append(stat)

        return filtered
