"""
Kungälv Energi DSO model implementation.

This module provides the EllevioFritidsHusDSO class for handling
Ellevio Fritidshus specific tariff calculations and configurations.

https://www.ellevio.se/abonnemang/elnatspriser/fritidshus/
"""

from typing import ClassVar

from .dsobase import DSOBase
from .models.average_of_x_days_model import AverageOfXDaysModel


class EllevioFritidsHusDSO(DSOBase, AverageOfXDaysModel):
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
        "months": list(range(1, 13)),
        "hours": list(range(6, 22)),
    }

    @classmethod
    def predicted_consumption(cls, energy_hour: float, power: int) -> float:
        """Return the expected peak value."""
        consumption = energy_hour + power / 1000

        return consumption if cls.tariff_active() else consumption * 0.5
