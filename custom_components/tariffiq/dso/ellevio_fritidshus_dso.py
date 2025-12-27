"""
Kungälv Energi DSO model implementation.

This module provides the EllevioFritidsHusDSO class for handling
Ellevio Fritidshus specific tariff calculations and configurations.
"""

from datetime import datetime
from typing import ClassVar

from .dsobase import DSOBase


class EllevioFritidsHusDSO(DSOBase):
    """Ellevio Fritidshus DSO model."""

    name: ClassVar[str] = "Ellevio Fritidshus"
    currency: ClassVar[str] = "SEK"
    fees: ClassVar[dict] = {  # Fuse size: fees
        "16-25": {
            "fixed_fee": 4740,
            "transfer_fee": 0.07,
            "tariff_cost": 81.25,
        },
        "35": {
            "fixed_fee": 11880,
            "transfer_fee": 0.07,
            "tariff_cost": 81.25,
        },
        "50": {
            "fixed_fee": 18180,
            "transfer_fee": 0.07,
            "tariff_cost": 81.25,
        },
        "63": {
            "fixed_fee": 26100,
            "transfer_fee": 0.07,
            "tariff_cost": 81.25,
        },
    }
    tariff_schedule: ClassVar[dict] = {
        "full": {
            "months": list(range(1, 13)),
            "hours": list(range(6, 22)),
        },
        "half": {
            "months": list(range(1, 13)),
            "hours": [22, 23, 0, 1, 2, 3, 4, 5],
        },
    }

    @classmethod
    def tariff_starts_at(cls, current_time: datetime | None = None) -> datetime | None:
        """Return the start time of the tariff period."""
        now = current_time or datetime.now()  # noqa: DTZ005

        if (
            now.month in cls.tariff_schedule["full"]["months"]
            and now.replace(day=now.day + 1).month
            in cls.tariff_schedule["full"]["months"]
        ):
            day = (
                now.day
                if now.hour < cls.tariff_schedule["full"]["hours"][0]
                else now.day + 1
            )

            return now.replace(
                day=day,
                hour=cls.tariff_schedule["full"]["hours"][0],
                minute=0,
                second=0,
                microsecond=0,
            )

        return None

    @classmethod
    def tariff_ends_at(cls, current_time: datetime | None = None) -> datetime | None:
        """Return the end time of the tariff period."""
        now = current_time or datetime.now()  # noqa: DTZ005

        if now.month in cls.tariff_schedule["full"]["months"]:
            return now.replace(
                hour=cls.tariff_schedule["full"]["hours"][-1] + 1,
                minute=0,
                second=0,
                microsecond=0,
            )

        return None

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        now = datetime.now()  # noqa: DTZ005

        return now.hour in cls.tariff_schedule["full"]["hours"]
