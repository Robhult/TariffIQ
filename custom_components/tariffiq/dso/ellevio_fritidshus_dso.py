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

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        now = datetime.now()  # noqa: DTZ005

        return now.hour in range(7, 21)
