"""Config flow for Wolf SmartSet Service integration."""
from __future__ import annotations
import logging
from typing import Any, Optional

import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_DEVICES, CONF_HOST, CONF_PORT
from .const import (
    DOMAIN,
    DEFAULT_HOST,
    DEFAULT_PORT,
    WOLF_DEVICES,
    WOLF_DEFAULT_DEVICES,
    DEVICE_INFO_NAME,
)

_LOGGER = logging.getLogger(__name__)

WOLF_HOST_SCHEMA = {
    vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
}

WOLF_DEVICE_SCHEMA = {}
for _device in WOLF_DEVICES:
    device_name = WOLF_DEVICES.get(_device, ["", "", "", ""])[DEVICE_INFO_NAME]
    device_is_default = _device in WOLF_DEFAULT_DEVICES
    WOLF_DEVICE_SCHEMA[vol.Optional(_device, default=device_is_default)] = cv.boolean


class WolfCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """wolf custom config flow"""

    data: Optional[dict[str, Any]]

    def __init__(self):
        """Initialize with empty host and port."""
        self.host = None
        self.port = None
        self.devices = None

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}

        if user_input is not None:

            self.host = user_input[CONF_HOST]
            self.port = user_input[CONF_PORT]

            return await self.async_step_device()

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(WOLF_HOST_SCHEMA), errors=errors
        )

    async def async_step_device(self, user_input: Optional[dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}

        if user_input is not None:

            # Input is valid, set data.
            self.devices = []
            for _device in WOLF_DEVICES:
                if user_input[_device]:
                    self.devices.append(_device)

            data = {
                CONF_HOST: self.host,
                CONF_PORT: self.port,
                CONF_DEVICES: self.devices,
            }

            # User is done adding repos, create the config entry.
            return self.async_create_entry(title="Wolf Climate Control ISM8", data=data)

        return self.async_show_form(
            step_id="device", data_schema=vol.Schema(WOLF_DEVICE_SCHEMA), errors=errors
        )
