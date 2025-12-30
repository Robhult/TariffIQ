"""Base DSO class for TariffIQ."""

from abc import ABC
from datetime import datetime
from typing import ClassVar


class DSOBase(ABC):
    """Base class for Distribution System Operators."""

    # Class attributes that each DSO must define
    name: ClassVar[str]
    currency: ClassVar[str]
    fees: ClassVar[dict]  # Fuse size: fees
    tariff_schedule: ClassVar[dict] = {}
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
    def tariff_starts_at(cls, current_time: datetime | None = None) -> datetime | None:
        """Return the start time of the tariff period."""
        now = current_time or datetime.now()  # noqa: DTZ005

        if (
            now.month in cls.tariff_schedule["months"]
            and now.replace(day=now.day + 1).month in cls.tariff_schedule["months"]
        ):
            day = now.day if now.hour < cls.tariff_schedule["hours"][0] else now.day + 1

            return now.replace(
                day=day,
                hour=cls.tariff_schedule["hours"][0],
                minute=0,
                second=0,
                microsecond=0,
            )

        return None

    @classmethod
    def tariff_ends_at(cls, current_time: datetime | None = None) -> datetime | None:
        """Return the end time of the tariff period."""
        now = current_time or datetime.now()  # noqa: DTZ005

        if now.month in cls.tariff_schedule["months"]:
            return now.replace(
                hour=cls.tariff_schedule["hours"][-1] + 1,
                minute=0,
                second=0,
                microsecond=0,
            )

        return None

    @classmethod
    def tariff_active(cls, current_time: datetime | None = None) -> bool:
        """Determine if tariff is active."""
        now = current_time or datetime.now()  # noqa: DTZ005

        return bool(
            now.month in cls.tariff_schedule["months"]
            and now.hour in cls.tariff_schedule["hours"]
        )

    @classmethod
    def fixed_cost(cls) -> float:
        """Return the fixed cost for this DSO."""
        now = datetime.now()  # noqa: DTZ005
        current_hour = (now - datetime(now.year, 1, 1)).total_seconds() // 3600  # noqa: DTZ001
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
    def predicted_consumption(cls, energy_hour: float, power: int) -> float:
        """Return the expected peak value."""
        return energy_hour + power / 1000 if cls.tariff_active() else 0.0
