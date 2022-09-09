"""
Support for Wolf heating system ISM via ISM8 adapter
"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
import logging
import socket
import asyncio
from homeassistant.const import CONF_HOST, CONF_PORT, Platform

from homeassistant.helpers.discovery import load_platform
import homeassistant.helpers.config_validation as cv
from pywolf8.ism8 import Ism8

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.SELECT, Platform.BINARY_SENSOR, Platform.BUTTON]


async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    """set up the custom component over the yaml configuration"""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """set up the custom component over the config entry"""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    _config = entry.data

    protocol: type[Ism8] = Ism8()
    hass.data[DOMAIN]["protocol"] = protocol
    coro = hass.loop.create_server(
        protocol.factory,
        host=_config[CONF_HOST],
        port=_config[CONF_PORT],
        family=socket.AF_INET,
    )
    task = hass.loop.create_task(coro)
    await task
    if task.done():
        _server = task.result()
        for soc in _server.sockets:
            _LOGGER.debug(
                "Listening for ISM8 on %s : %s", soc.getsockname(), _config[CONF_PORT]
            )

    # Forward the setup to the sensor platform.
    for sensor in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, sensor)
        )
    return True
