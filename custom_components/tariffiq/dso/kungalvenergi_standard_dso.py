"""
Kungälv Energi DSO model implementation.

This module provides the KungalvEnergiDSO class for handling
Kungälv Energi specific tariff calculations and configurations.
"""

from datetime import datetime
from typing import ClassVar

from .dsobase import DSOBase


class KungalvEnergiStandardDSO(DSOBase):
    """Kungälv Energi Standard DSO model."""

    name: ClassVar[str] = "Kungälv Energi - Standard"
    currency: ClassVar[str] = "SEK"
    fees: ClassVar[dict] = {  # Fuse size: fees
        "16": {
            "fixed_fee": 4230,
            "transfer_fee": 0.5266,
            "tariff_cost": 57.17,
        },
        "20": {
            "fixed_fee": 5154,
            "transfer_fee": 0.5266,
            "tariff_cost": 57.17,
        },
        "25": {
            "fixed_fee": 6309,
            "transfer_fee": 0.5266,
            "tariff_cost": 57.17,
        },
        "35": {
            "fixed_fee": 8620,
            "transfer_fee": 0.5266,
            "tariff_cost": 57.17,
        },
        "50": {
            "fixed_fee": 12086,
            "transfer_fee": 0.5266,
            "tariff_cost": 57.17,
        },
        "63": {
            "fixed_fee": 15090,
            "transfer_fee": 0.5266,
            "tariff_cost": 57.17,
        },
    }
    tariff_schedule: ClassVar[dict] = {
        "months": [1, 2, 3, 11, 12],
        "hours": list(range(7, 21)),
    }

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
