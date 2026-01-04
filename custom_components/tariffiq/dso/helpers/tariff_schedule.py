"""Module for defining time patterns for DSO tariffs."""

from datetime import datetime, timedelta
from enum import Enum

from homeassistant.util import dt as dt_util

ALL_HOURS = list(range(24))
ALL_WEEKDAYS = list(range(7))  # 0=Monday, 6=Sunday
ALL_MONTHS = list(range(1, 13))
ALL_QUARTERS = list(range(1, 5))


class CalendarPeriods(Enum):
    """Enumeration for calendar periods used in time patterns."""

    Hour = "hour"
    Weekday = "weekday"  # 0=Monday, 6=Sunday
    Month = "month"
    Quarter = "quarter"


class TimePattern:
    """Class for defining time patterns for DSO tariffs."""

    def __init__(
        self,
        tariff_factor: float = 1.0,
        time_filters: dict[CalendarPeriods, list[int] | None] | None = None,
    ) -> None:
        """
        Initialize the TimePattern class.

        Args:
            tariff_factor: Multiplication factor for the time pattern, used in DSO.
            time_filters: Dictionary with keys as CalendarPeriods enum members
                         and values as lists of integers or None.
                         If nothing is set all values are included.

        """
        self.tariff_factor = tariff_factor

        if time_filters is None:
            time_filters = {}

        self.hour = time_filters.get(CalendarPeriods.Hour) or ALL_HOURS
        self.weekday = time_filters.get(CalendarPeriods.Weekday) or ALL_WEEKDAYS
        self.month = time_filters.get(CalendarPeriods.Month) or ALL_MONTHS
        self.quarter = time_filters.get(CalendarPeriods.Quarter) or ALL_QUARTERS

    def active(self, date: datetime | None = None) -> bool:
        """Check if a given datetime matches the time pattern."""
        if date is None:
            date = dt_util.now()

        return (
            date.hour in self.hour
            and date.weekday() in self.weekday
            and date.month in self.month
            and ((date.month - 1) // 3 + 1) in self.quarter
        )

    def starts_at(self, from_date: datetime | None = None) -> datetime:
        """Get the next datetime when the time pattern becomes active."""
        if from_date is None:
            from_date = dt_util.now()

        check_date = from_date.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )

        while True:
            if self.active(check_date):
                return check_date
            check_date += timedelta(hours=1)

    def ends_at(self, from_date: datetime | None = None) -> datetime:
        """Get the datetime when the time pattern ends."""
        if from_date is None:
            from_date = dt_util.now()

        check_date = from_date.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )

        while True:
            if not self.active(check_date):
                return check_date
            check_date += timedelta(hours=1)


class TariffSchedule:
    """Class for defining tariff schedules for DSOs."""

    def __init__(self, timepattern: list[TimePattern] | TimePattern) -> None:
        """TariffSchedule constructor."""
        self.timepatterns: list[TimePattern] = []
        self.hour: list[int] = []
        self.weekday: list[int] = []
        self.month: list[int] = []
        self.quarter: list[int] = []

        if isinstance(timepattern, TimePattern):
            self.timepatterns = [timepattern]
        else:
            self.timepatterns = timepattern

        for pattern in self.timepatterns:
            self.hour = list(set(self.hour) | set(pattern.hour))
            self.weekday = list(set(self.weekday) | set(pattern.weekday))
            self.month = list(set(self.month) | set(pattern.month))
            self.quarter = list(set(self.quarter) | set(pattern.quarter))

    def get_timepatterns(self) -> list[TimePattern]:
        """Get all TimePatterns in the TariffSchedule."""
        return self.timepatterns

    def active_timepattern(self, date: datetime | None = None) -> TimePattern | None:
        """Get the active TimePattern for a given datetime."""
        if date is None:
            date = dt_util.now()

        for timepattern in self.timepatterns:
            if timepattern.active(date):
                return timepattern

        return None

    def active(self, date: datetime | None = None) -> bool:
        """Check if any time pattern is active for a given datetime."""
        return self.active_timepattern(date) is not None

    def starts_at(self, from_date: datetime | None = None) -> datetime | None:
        """Get the next datetime when the time pattern becomes active."""
        if (
            self.hour == ALL_HOURS
            and self.weekday == ALL_WEEKDAYS
            and self.month == ALL_MONTHS
            and self.quarter == ALL_QUARTERS
        ):
            return None

        if from_date is None:
            from_date = dt_util.now()

        check_date = from_date.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )

        while True:
            if self.active(check_date):
                return check_date
            check_date += timedelta(hours=1)

    def ends_at(self, from_date: datetime | None = None) -> datetime | None:
        """Get the datetime when the time pattern ends."""
        if (
            self.hour == ALL_HOURS
            and self.weekday == ALL_WEEKDAYS
            and self.month == ALL_MONTHS
            and self.quarter == ALL_QUARTERS
        ):
            return None

        if from_date is None:
            from_date = dt_util.now()

        check_date = from_date.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )

        while True:
            if not self.active(check_date):
                return check_date
            check_date += timedelta(hours=1)
