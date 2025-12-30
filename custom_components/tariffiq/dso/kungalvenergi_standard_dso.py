"""
Kungälv Energi DSO model implementation.

This module provides the KungalvEnergiDSO class for handling
Kungälv Energi specific tariff calculations and configurations.

https://www.kungalvenergi.se/elnat/ny-effekttaxa/
"""

from typing import ClassVar

from custom_components.tariffiq.dso.models.average_of_x_hours_model import (
    AverageOfXHoursModel,
)

from .dsobase import DSOBase


class KungalvEnergiStandardDSO(DSOBase, AverageOfXHoursModel):
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
    tariff_schedule: ClassVar[dict] = {
        "months": [1, 2, 3, 11, 12],
        "days_in_week": list(range(7)),
        "hours": list(range(7, 21)),
    }
