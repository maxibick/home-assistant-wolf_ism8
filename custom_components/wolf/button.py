"""
Support for Wolf heating via ISM8 adapter
"""
import logging
from pywolf8.ism8 import Ism8
from collections.abc import Callable
from homeassistant import config_entries
from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_DEVICES
from homeassistant.helpers.typing import HomeAssistantType
from .const import (
    DEVICE_INFO_MODELL,
    DEVICE_INFO_SW_VERSION,
    DOMAIN,
    DEVICE_INFO_NAME,
    DEVICE_INFO_MANUFACTURER,
    WOLF_DEVICES,
    SensorType,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: Callable,
):
    """
    performs setup of the analog sensors, expects a
    reference to an ism8-adapter via hass.data
    """

    config = hass.data[DOMAIN][config_entry.entry_id]
    ism8: Ism8 = hass.data[DOMAIN]["protocol"]

    sensors = []
    for nbr in ism8.get_all_sensors().keys():

        if ism8.get_device(nbr) in config[CONF_DEVICES]:

            if ism8.get_type(nbr) == SensorType.DPT_SWITCH and nbr in [194, 193]:
                sensors.append(WolfButton(ism8, nbr))

    async_add_entities(sensors)


class WolfButton(ButtonEntity):
    """
    Implementation of Wolf Heating System Sensor via ISM8-network adapter
    dp_nbr represents the unique identifier of the up to 200 different
    sensors
    """

    def __init__(self, ism8: Ism8, dp_nbr: int) -> None:
        self.dp_nbr = dp_nbr
        self._device = ism8.get_device(dp_nbr)
        self._name = ism8.get_name(dp_nbr)
        self._type = ism8.get_type(dp_nbr)
        self._ism8 = ism8
        _LOGGER.debug("setup button no. %d as %s", self.dp_nbr, self._type)

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique_id of this sensor."""
        return "wolf." + self._device.lower().replace(" ", "") + "." + str(self.dp_nbr)

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._device)
            },
            "name": WOLF_DEVICES.get(self._device, ("", "", "", ""))[DEVICE_INFO_NAME],
            "manufacturer": WOLF_DEVICES.get(self._device, ("", "", "", ""))[
                DEVICE_INFO_MANUFACTURER
            ],
            "model": WOLF_DEVICES.get(self._device, ("", "", "", ""))[
                DEVICE_INFO_MODELL
            ],
            "sw_version": WOLF_DEVICES.get(self._device, ("", "", "", ""))[
                DEVICE_INFO_SW_VERSION
            ],
        }

    @property
    def icon(self):
        """Return icon"""
        if self.dp_nbr == 194:
            return "mdi:water-thermometer"
        return "mdi:button-pointer"

    async def async_press(self) -> None:
        """Handle the button press."""
        self._ism8.send_dp_value(self.dp_nbr, 1)
