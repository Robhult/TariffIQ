"""
Ellevio Lägenhet DSO model implementation.

This module provides the EllevioLgh30DSO class for handling
Ellevio Lägenhet specific tariff calculations and configurations.
"""

from typing import ClassVar

from .dsobase import DSOBase


class EllevioLgh30DSO(DSOBase):
    """Ellevio Lägenhet grupp <30st DSO model."""

    name: ClassVar[str] = "Ellevio Lägenhet grupp <30st"
    currency: ClassVar[str] = "SEK"
    fees: ClassVar[dict] = {  # Fuse size: fees
        "Default": {
            "fixed_fee": 1320,
            "transfer_fee": 0.26,
            "tariff_cost": 0,
        }
    }

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        return False
