"""DSO registry for TariffIQ."""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import Any

from custom_components.tariffiq.helpers import LOGGER

# Simple DSO registry
DSO_REGISTRY: dict[str, dict[str, Any]] = {}


def _discover_and_import_dso_classes() -> list[Any]:
    """Dynamically discover and import DSO classes."""
    dso_classes = []

    try:
        # Import base class first
        from .dsobase import DSOBase  # noqa: PLC0415

        # Get the current package directory
        current_dir = Path(__file__).parent

        # Find all *_dso.py files
        for file_path in current_dir.glob("*_dso.py"):
            module_name = file_path.stem  # filename without .py

            try:
                # Import the module-this happens at module load time, not in event loop
                module = importlib.import_module(f".{module_name}", package=__package__)

                # Find DSO classes in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        inspect.isclass(attr)
                        and issubclass(attr, DSOBase)
                        and attr != DSOBase
                    ):
                        dso_classes.append(attr)
                        LOGGER.debug(
                            "Discovered DSO class: %s from %s", attr.name, module_name
                        )

            except (ImportError, AttributeError, ModuleNotFoundError) as e:
                LOGGER.warning("Could not import DSO module %s: %s", module_name, e)

    except (ImportError, OSError) as e:
        LOGGER.error("Error during DSO discovery: %s", e)

    return dso_classes


def _populate_registry() -> None:
    """Populate the registry from discovered DSO classes."""
    dso_classes = _discover_and_import_dso_classes()

    for dso_class in dso_classes:
        try:
            DSO_REGISTRY[dso_class.name] = {
                "name": getattr(dso_class, "name", "Unknown DSO"),
                "currency": getattr(dso_class, "currency", "SEK"),
                "fees": getattr(dso_class, "fees", {}),
                "class": dso_class,
            }
        except (AttributeError, TypeError) as e:
            LOGGER.warning("Error registering DSO %s: %s", dso_class.name, e)


def get_dso_data(name: str) -> dict[str, Any] | None:
    """Get DSO data by name."""
    return DSO_REGISTRY.get(name)


def get_available_dsos() -> list[str]:
    """Get list of available DSO names."""
    return list(DSO_REGISTRY.keys())


def get_dso_fuse_sizes(dso_name: str) -> list[str]:
    """Get fuse sizes for a specific DSO."""
    dso_data = DSO_REGISTRY.get(dso_name, {})
    fees = dso_data.get("fees", {})
    return list(fees.keys())


def get_dso_class(dso_name: str) -> Any:
    """Get DSO class by name."""
    dso_data = DSO_REGISTRY.get(dso_name, {})
    return dso_data.get("class")


def get_fuse_sizes_for_dso_class(dso_class: Any) -> list[str]:
    """Get fuse sizes directly from a DSO class."""
    if hasattr(dso_class, "fees"):
        return list(dso_class.fees.keys())
    return []


# Populate registry on module import
_populate_registry()
