import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .api import ThermiaHeatPumpAPI
from .const import DOMAIN, CONF_REGISTER, CONF_VALUE

_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: ConfigType):
    def handle_set_register(call):
        register = call.data[CONF_REGISTER]
        value = call.data[CONF_VALUE]
        api = hass.data[DOMAIN]["api"]
        try:
            api.set_register(register, value)
            _LOGGER.info(f"Set register {register} to {value}")
        except Exception as e:
            _LOGGER.error(f"Failed to set register {register}: {str(e)}")

    hass.services.register(DOMAIN, "set_register", handle_set_register)
    return True

def setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["api"] = ThermiaHeatPumpAPI(
        entry.data["username"],
        entry.data["password"]
    )
    return True
