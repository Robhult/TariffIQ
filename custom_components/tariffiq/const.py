"""Constants for tariffiq."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "tariffiq"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

NONE = "None"

PRICING_INTEGRATIONS = ["nordpool", "entso_e"]
DSO_MODELS = [
    "Kungälv Energi - Standard",
    "Kungälv Energi - Lägenhet",
    "Kungälv Energi - Lågspänning>63A",
    "Kungälv Energi - Högspänning",
]

# Config flow constants
CONF_NAME = "name"
CONF_POWER_SENSOR = "power_sensor"
CONF_ENERGY_SENSOR = "energy_sensor"
CONF_DSO_AND_MODEL = "dso_and_model"
CONF_PRICING_ENTITY = "pricing_entity"
