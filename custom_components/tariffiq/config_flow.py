"""Configuration flow for TariffIQ integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import ATTR_NAME, ATTR_UNIT_OF_MEASUREMENT
from homeassistant.helpers import selector, template

from .const import (
    CONF_DSO_AND_MODEL,
    CONF_ENERGY_SENSOR,
    CONF_NAME,
    CONF_POWER_SENSOR,
    CONF_PRICING_ENTITY,
    DOMAIN,
    DSO_MODELS,
    NONE,
    PRICING_INTEGRATIONS,
)
from .helpers import LOGGER


class TariffIQConfigFlow(ConfigFlow, domain=DOMAIN):  # pyright: ignore[reportCallIssue]
    """Config flow for TariffIQ."""

    VERSION = 1
    data = None
    options = None

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
        self._async_abort_entries_match()

        _errors: dict[str, str] = {}

        _schema = vol.Schema(
            {
                vol.Required(CONF_NAME, "TariffIQ"): str,
                vol.Required(CONF_DSO_AND_MODEL): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=DSO_MODELS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
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
                vol.Optional(CONF_PRICING_ENTITY): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=self._get_pricing_entities())
                ),
            }
        )

        if user_input is not None:
            self.data = user_input

            # dso and model validation
            if self.data[CONF_DSO_AND_MODEL] not in DSO_MODELS:
                _errors[CONF_DSO_AND_MODEL] = "invalid_dso_model"

            # Power sensor validation
            if not self.data[CONF_POWER_SENSOR].startswith("sensor."):
                _errors[CONF_POWER_SENSOR] = "invalid_power_sensor"
            val_state = self.hass.states.get(self.data[CONF_POWER_SENSOR])
            if val_state is None or not isinstance(float(val_state.state), float):
                _errors[CONF_POWER_SENSOR] = "invalid_value_power_sensor"

            # Energy sensor validation
            if not self.data[CONF_ENERGY_SENSOR].startswith("sensor."):
                _errors[CONF_ENERGY_SENSOR] = "invalid_energy_sensor"
            val_state = self.hass.states.get(self.data[CONF_ENERGY_SENSOR])
            if val_state is None or not isinstance(float(val_state.state), float):
                _errors[CONF_ENERGY_SENSOR] = "invalid_value_energy_sensor"

            # pricing entity validation
            self.options = {}
            _pricing_entity = self.hass.states.get(self.data[CONF_PRICING_ENTITY])
            if _pricing_entity is not None:
                try:
                    if _pricing_entity:
                        self.options[ATTR_UNIT_OF_MEASUREMENT] = (
                            _pricing_entity.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
                        )
                except (IndexError, KeyError):
                    _errors[CONF_PRICING_ENTITY] = "error_extracting_currency"

            if _errors:
                return self.async_show_form(
                    step_id="user",
                    data_schema=_schema,
                    errors=_errors,
                )

            await self.async_set_unique_id(self.data[CONF_NAME])
            self._abort_if_unique_id_configured()

            LOGGER.debug(
                'Creating entry "%s" with data "%s"',
                self.unique_id,
                self.data,
            )
            return self.async_create_entry(
                title=self.data.get(
                    CONF_NAME, DOMAIN
                ),  # TODO: Update to a better title.
                data=self.data,
                options=self.options,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_schema,
            errors=_errors,
        )
