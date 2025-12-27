"""Base DSO class for TariffIQ."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar

from custom_components.tariffiq.const import NOTIMPLEMENTED_MSG


class DSOBase(ABC):
    """Base class for Distribution System Operators."""

    # Class attributes that each DSO must define
    name: ClassVar[str]
    currency: ClassVar[str]
    fees: ClassVar[dict]  # Fuse size: fees
    tariff_schedule: ClassVar[dict] = {}

    selected_fees: dict

    def __init__(self, fuse_size: str) -> None:
        """Initialize the DSO class."""
        self.selected_fees = self.fees[fuse_size]

    @classmethod
    def get_fuse_sizes(cls) -> list[str]:
        """Return all available fuse sizes for this DSO (combined model approach)."""
        return list(cls.fees.keys())

    @classmethod
    def tariff_starts_at(cls) -> datetime | None:
        """Return the start time of the tariff period."""
        return None

    @classmethod
    def tariff_ends_at(cls) -> datetime | None:
        """Return the end time of the tariff period."""
        return None

    @classmethod
    @abstractmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is currently active."""
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    def fixed_cost(self) -> float:
        """Return the fixed cost for this DSO."""
        now = datetime.now()  # noqa: DTZ005
        current_hour = (now - datetime(now.year, 1, 1)).total_seconds() // 3600  # noqa: DTZ001
        total_hours_in_year = (
            datetime(now.year + 1, 1, 1) - datetime(now.year, 1, 1)  # noqa: DTZ001
        ).total_seconds() // 3600

        fixed_fee = self.selected_fees.get("fixed_fee", 0)

        return fixed_fee * current_hour / total_hours_in_year

    def variable_cost(self, energy_value: float) -> float:
        """Return the variable cost for this DSO based on energy consumption."""
        # Calculate variable cost based on energy consumption
        transfer_fee = self.selected_fees.get("transfer_fee", 0)

        return energy_value * transfer_fee
