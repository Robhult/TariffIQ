"""Constants for tariffiq."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "tariffiq"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

NONE = "None"
Default = "Default"

PRICING_INTEGRATIONS = ["nordpool", "entso_e"]
DSO = {
    "Kungälv Energi": {
        "models": {
            "Standard": {
                "fuse_sizes": {
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
                },
                "tariff_months": {
                    1: 1.0,
                    2: 1.0,
                    3: 1.0,
                    4: 0.0,
                    5: 0.0,
                    6: 0.0,
                    7: 0.0,
                    8: 0.0,
                    9: 0.0,
                    10: 0.0,
                    11: 1.0,
                    12: 1.0,
                },
                "tariff_hours": {
                    0: 0.0,
                    1: 0.0,
                    2: 0.0,
                    3: 0.0,
                    4: 0.0,
                    5: 0.0,
                    6: 0.0,
                    7: 1.0,
                    8: 1.0,
                    9: 1.0,
                    10: 1.0,
                    11: 1.0,
                    12: 1.0,
                    13: 1.0,
                    14: 1.0,
                    15: 1.0,
                    16: 1.0,
                    17: 1.0,
                    18: 1.0,
                    19: 1.0,
                    20: 1.0,
                    21: 1.0,
                    22: 0.0,
                    23: 0.0,
                },
            },
            "Lägenhet": {
                "fuse_sizes": {
                    "16": {
                        "fixed_fee": 2479,
                        "transfer_fee": 0.6963,
                        "tariff_cost": 0,
                    }
                },
            },
            # "Lågspänning>63A",
            # "Högspänning",
        },
        "currency": "SEK",
        "model_module": "kungalvenergi",
        "model_class": "KungalvEnergiModel",
    },
    "Ellevio": {
        "models": {
            "Hus": {
                "fuse_sizes": {
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
                },
                "tariff_months": {
                    1: 1.0,
                    2: 1.0,
                    3: 1.0,
                    4: 1.0,
                    5: 1.0,
                    6: 1.0,
                    7: 1.0,
                    8: 1.0,
                    9: 1.0,
                    10: 1.0,
                    11: 1.0,
                    12: 1.0,
                },
                "tariff_hours": {
                    0: 0.5,
                    1: 0.5,
                    2: 0.5,
                    3: 0.5,
                    4: 0.5,
                    5: 0.5,
                    6: 0.5,
                    7: 1.0,
                    8: 1.0,
                    9: 1.0,
                    10: 1.0,
                    11: 1.0,
                    12: 1.0,
                    13: 1.0,
                    14: 1.0,
                    15: 1.0,
                    16: 1.0,
                    17: 1.0,
                    18: 1.0,
                    19: 1.0,
                    20: 1.0,
                    21: 1.0,
                    22: 0.5,
                    23: 0.5,
                },
            },
            "Lägenhet": {
                "fuse_sizes": {
                    "Default": {
                        "fixed_fee": 1440,
                        "transfer_fee": 0.26,
                        "tariff_cost": 0,
                    }
                },
                "Lägenhet30": {
                    "fuse_sizes": {
                        "Default": {
                            "fixed_fee": 1320,
                            "transfer_fee": 0.26,
                            "tariff_cost": 0,
                        }
                    },
                },
                "Lägenhet60": {
                    "fuse_sizes": {
                        "Default": {
                            "fixed_fee": 1200,
                            "transfer_fee": 0.26,
                            "tariff_cost": 0,
                        }
                    },
                },
                "Lägenhet100": {
                    "fuse_sizes": {
                        "Default": {
                            "fixed_fee": 1080,
                            "transfer_fee": 0.755,
                            "tariff_cost": 0,
                        }
                    },
                },
                "Fritidshus": {
                    "fuse_sizes": {
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
                    },
                    "tariff_months": {
                        1: 1.0,
                        2: 1.0,
                        3: 1.0,
                        4: 1.0,
                        5: 1.0,
                        6: 1.0,
                        7: 1.0,
                        8: 1.0,
                        9: 1.0,
                        10: 1.0,
                        11: 1.0,
                        12: 1.0,
                    },
                    "tariff_hours": {
                        0: 0.5,
                        1: 0.5,
                        2: 0.5,
                        3: 0.5,
                        4: 0.5,
                        5: 0.5,
                        6: 0.5,
                        7: 1.0,
                        8: 1.0,
                        9: 1.0,
                        10: 1.0,
                        11: 1.0,
                        12: 1.0,
                        13: 1.0,
                        14: 1.0,
                        15: 1.0,
                        16: 1.0,
                        17: 1.0,
                        18: 1.0,
                        19: 1.0,
                        20: 1.0,
                        21: 1.0,
                        22: 0.5,
                        23: 0.5,
                    },
                },
            },
            "currency": "SEK",
            "model_module": "ellevio",
            "model_class": "EllevioModel",
        },
    },
}

# Config flow constants
CONF_NAME = "name"
CONF_POWER_SENSOR = "power_sensor"
CONF_ENERGY_SENSOR = "energy_sensor"
CONF_DSO = "dso"
CONF_DSO_MODEL = "dso_model"
CONF_FUSE_SIZE = "fuse_size"
CONF_PRICING_ENTITY = "pricing_entity"
