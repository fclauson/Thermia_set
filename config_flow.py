import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
})

class ThermiaSetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Thermia Set integration."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user provides credentials."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_credentials(
                user_input["username"], user_input["password"]
            )
            if valid:
                return self.async_create_entry(
                    title="Thermia Heat Pump",
                    data={
                        "username": user_input["username"],
                        "password": user_input["password"],
                    },
                )
            else:
                self._errors["base"] = "auth"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=self._errors
        )

    async def _test_credentials(self, username, password):
        """Return true if credentials are valid."""
        try:
            from thermia import ThermiaOnline
            client = ThermiaOnline(username, password)
            await self.hass.async_add_executor_job(client.authenticate)
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to authenticate with Thermia: {str(e)}")
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ThermiaSetOptionsFlow(config_entry)

class ThermiaSetOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Thermia Set integration."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("option_1", default=self.config_entry.options.get("option_1", "default_value")): str,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
