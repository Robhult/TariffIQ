"""
Ellevio Lägenhet DSO model implementation.

This module provides the EllevioLghDSO class for handling
Ellevio Lägenhet specific tariff calculations and configurations.
"""

from typing import ClassVar

from .dsobase import DSOBase


class EllevioLghDSO(DSOBase):
    """Ellevio Lägenhet DSO model."""

    name: ClassVar[str] = "Ellevio Lägenhet"
    currency: ClassVar[str] = "SEK"
    fees: ClassVar[dict] = {  # Fuse size: fees
        "Default": {
            "fixed_fee": 1440,
            "transfer_fee": 0.26,
            "tariff_cost": 0,
        }
    }

    @classmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is active."""
        return False
