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

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        now = datetime.now()  # noqa: DTZ005

        return now.month in [11, 12, 1, 2, 3] and now.hour in range(7, 22)
