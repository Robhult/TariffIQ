"""
Kungälv Energi DSO model implementation.

This module provides the EllevioHusDSO class for handling
Ellevio Hus specific tariff calculations and configurations.

https://www.ellevio.se/abonnemang/elnatspriser/hus/
"""

from typing import ClassVar

from custom_components.tariffiq.dso.helpers.tariff_schedule import (
    CalendarPeriods,
    TariffSchedule,
    TimePattern,
)

from .dsobase import DSOBase
from .models.average_of_x_days_model import AverageOfXDaysModel


class EllevioHusDSO(DSOBase, AverageOfXDaysModel):
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
        "months": list(range(1, 13)),
        "hours": list(range(6, 22)),
    }
    tariff_schedule_new: ClassVar[TariffSchedule] = TariffSchedule(
        [
            TimePattern(
                tariff_factor=0.5,
                time_filters={
                    CalendarPeriods.Hour: [22, 23, 0, 1, 2, 3, 4, 5],
                },
            ),
            TimePattern(
                tariff_factor=1.0,
                time_filters={
                    CalendarPeriods.Hour: list(range(6, 22)),
                },
            ),
        ]
    )

    @classmethod
    def predicted_consumption(cls, energy_hour: float, power: int) -> float:
        """Return the expected peak value."""
        consumption = energy_hour + power / 1000

        return consumption if cls.tariff_active() else consumption * 0.5
