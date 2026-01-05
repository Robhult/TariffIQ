"""Base DSO class for TariffIQ."""

from abc import ABC
from datetime import datetime
from typing import ClassVar

from homeassistant.util import dt as dt_util

from custom_components.tariffiq.dso.helpers.tariff_schedule import TariffSchedule


class DSOBase(ABC):
    """Base class for Distribution System Operators."""

    # Class attributes that each DSO must define
    name: ClassVar[str]
    currency: ClassVar[str]
    fees: ClassVar[dict]  # Fuse size: fees
    tariff_schedule: ClassVar[TariffSchedule]
    selected_fees: dict

    @classmethod
    def __init__(cls, fuse_size: str) -> None:
        """Initialize the DSO class."""
        cls.selected_fees = cls.fees[fuse_size]

    @classmethod
    def get_fuse_sizes(cls) -> list[str]:
        """Return all available fuse sizes for this DSO (combined model approach)."""
        return list(cls.fees.keys())

    @classmethod
    def get_tariff_schedule(cls) -> list[dict[str, object]]:
        """Return the tariff schedule for this DSO."""
        return [
            {
                "tariff_factor": str(pattern.tariff_factor),
                "hours": pattern.hour if pattern.hour != list(range(24)) else "all",
                "weekdays": "pattern.weekday"
                if pattern.weekday != list(range(7))
                else "all",
                "months": pattern.month
                if pattern.month != list(range(1, 13))
                else "all",
            }
            for pattern in cls.tariff_schedule.timepatterns
        ]

    @classmethod
    def tariff_starts_at(cls, current_time: datetime | None = None) -> datetime | None:
        """Return the start time of the tariff period."""
        return cls.tariff_schedule.starts_at(current_time)

    @classmethod
    def tariff_ends_at(cls, current_time: datetime | None = None) -> datetime | None:
        """Return the end time of the tariff period."""
        return cls.tariff_schedule.ends_at(current_time)

    @classmethod
    def tariff_active(cls, current_time: datetime | None = None) -> bool:
        """Determine if tariff is active."""
        return cls.tariff_schedule.active(current_time)

    @classmethod
    def fixed_cost(cls) -> float:
        """Return the fixed cost for this DSO."""
        now = dt_util.now()
        start_of_year = now.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        current_hour = (now - start_of_year).total_seconds() // 3600
        total_hours_in_year = (
            datetime(now.year + 1, 1, 1) - datetime(now.year, 1, 1)  # noqa: DTZ001
        ).total_seconds() // 3600

        fixed_fee = cls.selected_fees.get("fixed_fee", 0)

        return fixed_fee * current_hour / total_hours_in_year

    @classmethod
    def variable_cost(cls, energy_value: float) -> float:
        """Return the variable cost for this DSO based on energy consumption."""
        # Calculate variable cost based on energy consumption
        transfer_fee = cls.selected_fees.get("transfer_fee", 0)

        return energy_value * transfer_fee

    @classmethod
    def tariff_cost(cls) -> float:
        """Return the tariff cost for this DSO."""
        return cls.selected_fees.get("tariff_cost", 0.0)

    @classmethod
    def predicted_consumption(cls, energy_hour: float, power: float) -> float:
        """Return the expected peak value."""
        timepattern = cls.tariff_schedule.active_timepattern()

        if timepattern is not None:
            return (energy_hour + power / 1000) * timepattern.tariff_factor

        return energy_hour + power / 1000 if cls.tariff_active() else 0.0

    @classmethod
    def calculated_peak(cls, energy_hour: float) -> float:
        """Return the charged peak value based on tariff schedule."""
        timepattern = cls.tariff_schedule.active_timepattern()

        if timepattern is not None:
            return energy_hour * timepattern.tariff_factor

        return energy_hour if cls.tariff_active() else 0.0
