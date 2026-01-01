"""Helper functions for TariffIQ integration."""

import logging

LOGGER = logging.getLogger(__name__)


def nametoid(input_string) -> str:
    """Convert a name string to an ID string."""
    if isinstance(input_string, str):
        return input_string.lower().replace(" ", "_").replace(",", "")
    return input_string
