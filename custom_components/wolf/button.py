"""
Support for Wolf heating via ISM8 adapter
"""
import logging
from pywolf8.ism8 import Ism8
from homeassistant.components.button import ButtonEntity
from .const import (
    DEVICE_INFO_MODELL,
    DEVICE_INFO_SW_VERSION,
    DOMAIN,
    DEVICE_INFO,
    DEVICE_INFO_NAME,
    DEVICE_INFO_MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """
    performs setup of the analog sensors, expects a
    reference to an ism8-adapter via hass.data
    """

    sensors = []
    ism8 = hass.data[DOMAIN]

    for nbr in ism8.get_all_sensors().keys():
        if ism8.get_device(nbr) in discovery_info:
            if nbr == 194:
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
    def name(self):
        """Return the name of this sensor."""
        return (self._device + "_" + self._name).lower().replace(" ", "_")

    @property
    def unique_id(self):
        """Return the unique_id of this sensor."""
        return "wolf." + self._device.lower().replace(" ", "") + "." + str(self.dp_nbr)

    @property
    def icon(self):
        """Return icon"""
        return "mdi:button-pointer"

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            "name": DEVICE_INFO.get(self._device, ("", "", "", ""))[DEVICE_INFO_NAME],
            "manufacturer": DEVICE_INFO.get(self._device, ("", "", "", ""))[
                DEVICE_INFO_MANUFACTURER
            ],
            "model": DEVICE_INFO.get(self._device, ("", "", "", ""))[
                DEVICE_INFO_MODELL
            ],
            "sw_version": DEVICE_INFO.get(self._device, ("", "", "", ""))[
                DEVICE_INFO_SW_VERSION
            ],
        }

    async def async_press(self) -> None:
        """Handle the button press."""

        self._ism8.send_dp_value(self.dp_nbr, 1)
