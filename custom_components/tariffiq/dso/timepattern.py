"""Module for defining time patterns for DSO tariffs."""

from enum import Enum
import time
from typing import ClassVar


class CalendarPeriods(Enum):
    """Enumeration for calendar periods used in time patterns."""

    Minute = "minute"
    Hour = "hour"
    Weekday = "weekday"
    Month = "month"
    Quarter = "quarter"


class TimePattern:
    """Class for defining time patterns for DSO tariffs."""

    _valid_minutes: ClassVar[list[int]] = list(range(60))
    _valid_hours: ClassVar[list[int]] = list(range(24))
    _valid_weekdays: ClassVar[list[int]] = list(range(7))  # 0=Monday, 6=Sunday
    _valid_months: ClassVar[list[int]] = list(range(1, 13))
    _valid_quarters: ClassVar[list[int]] = list(range(1, 5))

    def __init__(
        self,
        tariff_factor: float = 1.0,
        time_filters: dict[CalendarPeriods, list[int] | None] | None = None,
    ) -> None:
        """
        Initialize the TimePattern class.

        Args:
            tariff_factor: Multiplication factor for the time pattern.
            time_filters: Dictionary with keys as CalendarPeriods enum members
                         and values as lists of integers or None.
                         If nothing is set all values are included.

        """
        self.tariff_factor = tariff_factor

        if time_filters is None:
            time_filters = {}

        if not self._validate(time_filters):
            raise ValueError("Invalid time filters provided.")  # noqa: EM101, TRY003

        self.minute = time_filters.get(CalendarPeriods.Minute, self._valid_minutes)
        self.hour = time_filters.get(CalendarPeriods.Hour, self._valid_hours)
        self.weekday = time_filters.get(CalendarPeriods.Weekday, self._valid_weekdays)
        self.month = time_filters.get(CalendarPeriods.Month, self._valid_months)
        self.quarter = time_filters.get(CalendarPeriods.Quarter, self._valid_quarters)

    def _validate(self, time_filters: dict[CalendarPeriods, list[int] | None]) -> bool:
        """Validate if the given time components match the time pattern."""
        return (
            time_filters.get(CalendarPeriods.Minute) in self._valid_minutes
            and time_filters.get(CalendarPeriods.Hour) in self._valid_hours
            and time_filters.get(CalendarPeriods.Weekday) in self._valid_weekdays
            and time_filters.get(CalendarPeriods.Month) in self._valid_months
            and time_filters.get(CalendarPeriods.Quarter) in self._valid_quarters
        )
