"""Configuration flow for TariffIQ integration."""

from __future__ import annotations

import secrets
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import selector, template

from .const import (
    CONF_DSO_AND_MODEL,
    CONF_ENERGY_SENSOR,
    CONF_FUSE_SIZE,
    CONF_NAME,
    CONF_POWER_SENSOR,
    DOMAIN,
    NONE,
    PRICING_INTEGRATIONS,
)
from .dso import get_available_dsos, get_dso_fuse_sizes
from .helpers import LOGGER


class TariffIQConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for TariffIQ."""

    VERSION = 1
    data: dict[str, Any] = {}  # noqa: RUF012
    options: dict[str, Any] = {}  # noqa: RUF012

    def _get_pricing_entities(self) -> list[str]:
        """Get pricing entities for the config flow."""
        _pricing_entities = [NONE]

        # Check for loaded pricing integrations and get their entities
        for integration_domain in PRICING_INTEGRATIONS:
            try:
                # Try to get entities from the integration
                entities = list(
                    template.integration_entities(self.hass, integration_domain)
                )
                if entities:  # Only add if we actually found entities
                    _pricing_entities.extend(entities)
                    LOGGER.debug(
                        "Found %d entities from %s integration",
                        len(entities),
                        integration_domain,
                    )
            except (KeyError, ValueError, AttributeError, LookupError) as e:
                LOGGER.debug(
                    "Could not get entities from %s: %s", integration_domain, e
                )

        return _pricing_entities

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle initial user step."""
        _errors: dict[str, str] = {}

        # Generate random default name
        default_name = f"TariffIQ_{secrets.token_hex(4)}"

        # Get available DSOs from registry
        available_dsos = get_available_dsos()

        _schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=default_name): str,
                vol.Required(CONF_DSO_AND_MODEL): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=available_dsos,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        if user_input is not None:
            self.data.update(user_input)

            # Set unique ID and abort if configured
            await self.async_set_unique_id(self.data[CONF_NAME])
            self._abort_if_unique_id_configured()

            # dso and model validation
            if self.data[CONF_DSO_AND_MODEL] not in list(available_dsos):
                _errors[CONF_DSO_AND_MODEL] = "invalid_dso_and_model"

            if _errors:
                return self.async_show_form(
                    step_id="user",
                    data_schema=_schema,
                    errors=_errors,
                    last_step=False,
                )

            return await self.async_step_dso_fuse_size()

        return self.async_show_form(
            step_id="user",
            data_schema=_schema,
            errors=_errors,
            last_step=False,
        )

    async def async_step_dso_fuse_size(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """DSO fuse step."""
        _errors: dict[str, str] = {}

        # Get available fuse sizes for the selected DSO and model
        available_fuses = get_dso_fuse_sizes(self.data[CONF_DSO_AND_MODEL])

        _schema = vol.Schema(
            {
                vol.Required(CONF_FUSE_SIZE): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=available_fuses,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        if user_input is not None:
            self.data.update(user_input)

            if self.data[CONF_FUSE_SIZE] not in list(available_fuses):
                _errors[CONF_FUSE_SIZE] = "invalid_fuse_size"

            if _errors:
                return self.async_show_form(
                    step_id="dso_fuse_size",
                    data_schema=_schema,
                    errors=_errors,
                    last_step=False,
                )

            return await self.async_step_sensor()

        return self.async_show_form(
            step_id="dso_fuse_size",
            data_schema=_schema,
            errors=_errors,
            last_step=False,
        )

    async def async_step_sensor(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Sensor step."""
        _errors: dict[str, str] = {}

        _schema = vol.Schema(
            {
                vol.Required(CONF_POWER_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="power",
                        multiple=False,
                    )
                ),
                vol.Required(CONF_ENERGY_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="energy",
                        multiple=False,
                    )
                ),
                # vol.Optional(CONF_PRICING_ENTITY): selector.SelectSelector(
                #     selector.SelectSelectorConfig(options=self._get_pricing_entities())
                # ),
            }
        )

        if user_input is not None:
            self.data.update(user_input)

            # Power sensor validation
            if not user_input[CONF_POWER_SENSOR].startswith("sensor."):
                _errors[CONF_POWER_SENSOR] = "invalid_power_sensor"
            val_state = self.hass.states.get(user_input[CONF_POWER_SENSOR])
            if val_state is None or not isinstance(float(val_state.state), float):
                _errors[CONF_POWER_SENSOR] = "invalid_value_power_sensor"

            # Energy sensor validation
            if not user_input[CONF_ENERGY_SENSOR].startswith("sensor."):
                _errors[CONF_ENERGY_SENSOR] = "invalid_energy_sensor"
            val_state = self.hass.states.get(user_input[CONF_ENERGY_SENSOR])
            if val_state is None or not isinstance(float(val_state.state), float):
                _errors[CONF_ENERGY_SENSOR] = "invalid_value_energy_sensor"

            # self.options = {}
            # _pricing_entity = self.hass.states.get(self.data[CONF_PRICING_ENTITY])
            # if _pricing_entity is not None:
            #     try:
            #         if _pricing_entity:
            #             self.options[ATTR_UNIT_OF_MEASUREMENT] = (
            #                 _pricing_entity.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
            #             )
            #     except (IndexError, KeyError):
            #         _errors[CONF_PRICING_ENTITY] = "error_extracting_currency"

            if _errors:
                return self.async_show_form(
                    step_id="sensor",
                    data_schema=_schema,
                    errors=_errors,
                    last_step=True,
                )

            LOGGER.debug(
                'Creating entry "%s" with data "%s"',
                self.unique_id,
                self.data,
            )
            return self.async_create_entry(
                title=self.data.get(CONF_NAME, DOMAIN),
                data=self.data,
                options=self.options,
            )

        return self.async_show_form(
            step_id="sensor",
            data_schema=_schema,
            errors=_errors,
            last_step=True,
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a TariffIQ options flow."""

    options: dict[str, Any] = {}  # noqa: RUF012

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize TariffIQ options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        # TODO: Start with a step where Fuse size can be changed.
        # Then show another step where the rest of the attributes can be changed.
        # tariff cost, fixed fee, etc. depending on DSO/model/fuse size.
        # TODO: Which options to be shown should be set depending on DSO object.
        # TODO: Default values should be set to those defined by the DSO. (Constants)

        return self.async_abort(reason="no_options_available")
