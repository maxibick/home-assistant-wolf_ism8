"""
Support for Wolf heating system ISM via ISM8 adapter
"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, WOLF_DEVICES, DEFAULT_WOLF_DEVICE, DEFAULT_PORT, DEFAULT_HOST
import logging
import socket
import asyncio
import voluptuous as vol
from homeassistant.const import CONF_DEVICES, CONF_HOST, CONF_PORT, Platform
from homeassistant.helpers.discovery import load_platform
import homeassistant.helpers.config_validation as cv
from pywolf8.ism8 import Ism8

REQUIREMENTS = ["pywolf8>=0.0.1"]

_LOGGER = logging.getLogger(__name__)

PLATFORM = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SELECT, Platform.BUTTON]

WOLF_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_DEVICES, default=[DEFAULT_WOLF_DEVICE]): vol.All(
            cv.ensure_list, [vol.In(WOLF_DEVICES)]
        ),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: WOLF_SCHEMA,
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    """Get all the config values, initialize network connection and add sensors"""
    _conf = config.get(DOMAIN)

    protocol: type[Ism8] = Ism8()
    hass.data[DOMAIN] = protocol
    coro = hass.loop.create_server(
        protocol.factory,
        host=_conf.get(CONF_HOST),
        port=_conf.get(CONF_PORT),
        family=socket.AF_INET,
    )
    task = hass.loop.create_task(coro)
    await task
    if task.done():
        _server = task.result()
        for soc in _server.sockets:
            _LOGGER.debug(
                "Listening for ISM8 on %s : %s", soc.getsockname(), _conf.get(CONF_PORT)
            )

    # register services
    def handle_request_all(call):
        """Handle the service call."""
        protocol.request_all_datapoints()

    hass.services.async_register(DOMAIN, "request_all", handle_request_all, WOLF_SCHEMA)
    # call sensor_init with DEVICES as indication for which DP to initialize
    for sensor in PLATFORM:
        load_platform(hass, sensor, DOMAIN, _conf.get(CONF_DEVICES), config)
    return True
