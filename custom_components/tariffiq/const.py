"""Constants for tariffiq."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DATA_HASS_CONFIG = "tariffiq_hass_config"
DOMAIN = "tariffiq"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

NONE = "None"
Default = "Default"

NOTIMPLEMENTED_MSG = "This method should be implemented by subclasses."

# Tariff enum values
TARIFF_NONE = "none"
TARIFF_LOW = "low"
TARIFF_HIGH = "high"
TARIFF_OPTIONS = [TARIFF_NONE, TARIFF_LOW, TARIFF_HIGH]

PRICING_INTEGRATIONS = ["nordpool", "entso_e"]

# Config flow constants
CONF_NAME = "name"
CONF_POWER_SENSOR = "power_sensor"
CONF_ENERGY_SENSOR = "energy_sensor"
CONF_DSO_AND_MODEL = "dso_and_model"
CONF_FUSE_SIZE = "fuse_size"
CONF_PRICING_ENTITY = "pricing_entity"
