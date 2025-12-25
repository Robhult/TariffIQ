"""DSO discovery and management utilities."""

import importlib
import inspect
from pathlib import Path

from custom_components.tariffiq.helpers import LOGGER

from .dsobase import DSOBase


def discover_dso_classes() -> dict[str, type[DSOBase]]:
    """
    Dynamically discover all DSO classes in the dso folder.

    Returns:
        Dictionary mapping DSO names to their class implementations.

    """
    dso_classes = {}

    # Get the dso directory path
    dso_dir = Path(__file__).parent

    # Iterate through all Python files in the dso directory
    for file_path in dso_dir.glob("*_dso.py"):
        module_name = file_path.stem  # filename without .py

        try:
            # Import the module dynamically
            module = importlib.import_module(
                f".{module_name}", package="custom_components.tariffiq.dso"
            )

            # Find all classes in the module that inherit from DSOBase
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, DSOBase) and obj is not DSOBase:
                    # Use the class's name attribute as the key
                    dso_classes[obj.name] = obj

        except (ImportError, AttributeError) as e:
            # Log but don't fail if a DSO module can't be loaded
            LOGGER.error(f"Could not load DSO module {module_name}: {e}")

    return dso_classes


def get_dso_class(dso_name: str) -> type[DSOBase] | None:
    """
    Get a specific DSO class by name.

    Args:
        dso_name: Name of the DSO to retrieve

    Returns:
        The DSO class or None if not found

    """
    dso_classes = discover_dso_classes()
    return dso_classes.get(dso_name)


def get_available_dsos() -> list[str]:
    """
    Get list of available DSO names.

    Returns:
        List of DSO names

    """
    return list(discover_dso_classes().keys())
