"""
Kungälv Energi DSO model implementation.

This module provides the KungalvEnergiLghDSO class for handling
Kungälv Energi specific tariff calculations and configurations.
"""

from typing import ClassVar

from .dsobase import DSOBase


class KungalvEnergiLghDSO(DSOBase):
    """Kungälv Energi Lägenhet DSO model."""

    name: ClassVar[str] = "Kungälv Energi - Lägenhet"
    currency: ClassVar[str] = "SEK"
    fees: ClassVar[dict] = {  # Fuse size: fees
        "16": {
            "fixed_fee": 2479,
            "transfer_fee": 0.6963,
            "tariff_cost": 0,
        },
    }

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        return False
