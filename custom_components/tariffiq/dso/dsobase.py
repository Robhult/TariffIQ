"""Base DSO class for TariffIQ."""

from abc import ABC, abstractmethod
from typing import ClassVar

from custom_components.tariffiq.const import NOTIMPLEMENTED_MSG


class DSOBase(ABC):
    """Base class for Distribution System Operators."""

    # Class attributes that each DSO must define
    name: ClassVar[str]
    currency: ClassVar[str]
    fees: ClassVar[dict]  # Fuse size: fees

    @classmethod
    def get_fuse_sizes(cls) -> list[str]:
        """Return all available fuse sizes for this DSO (combined model approach)."""
        return list(cls.fees.keys())

    @classmethod
    @abstractmethod
    def tariff_active(cls) -> bool:
        """Determine if tariff is currently active."""
        raise NotImplementedError(NOTIMPLEMENTED_MSG)
