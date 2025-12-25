"""
Ellevio Lägenhet DSO model implementation.

This module provides the EllevioLgh100DSO class for handling
Ellevio Lägenhet specific tariff calculations and configurations.
"""

from typing import ClassVar

from .dsobase import DSOBase


class EllevioLgh100DSO(DSOBase):
    """Ellevio Lägenhet grupp 100st DSO model."""

    name: ClassVar[str] = "Ellevio Lägenhet grupp 100st"
    currency: ClassVar[str] = "SEK"
    fees: ClassVar[dict] = {  # Fuse size: fees
        "Default": {
            "fixed_fee": 1080,
            "transfer_fee": 0.755,
            "tariff_cost": 0,
        }
    }

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        # Alla månader, 22-06 full tariff, 07-21 halv tariff
        return True
