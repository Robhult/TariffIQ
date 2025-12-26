"""
Kungälv Energi DSO model implementation.

This module provides the EllevioHusDSO class for handling
Ellevio Hus specific tariff calculations and configurations.
"""

from datetime import datetime
from typing import ClassVar

from .dsobase import DSOBase


class EllevioHusDSO(DSOBase):
    """Ellevio Hus DSO model."""

    name: ClassVar[str] = "Ellevio Hus"
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
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        now = datetime.now()  # noqa: DTZ005

        return now.hour in cls.tariff_schedule["full"]["hours"]
