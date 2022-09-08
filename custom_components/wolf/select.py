"""
Support for Wolf heating via ISM8 adapter
"""

import logging
from homeassistant.components.select import SelectEntity
from pywolf8.ism8 import Ism8
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
            if ism8.get_type(nbr) in (
                "DPT_HVACContrMode",
                "DPT_HVACMode",
                "DPT_DHWMode",
            ):
                sensors.append(WolfSelect(ism8, nbr))
    async_add_entities(sensors)


class WolfSelect(SelectEntity):
    """Implementation of Wolf Heating System Sensor via ISM8-network adapter
    dp_nbr represents the unique identifier of the up to 200 different
    sensors
    """

    _attr_current_option = None

    def __init__(self, ism8: Ism8, dp_nbr: int) -> None:
        self.dp_nbr = dp_nbr
        self._device = ism8.get_device(dp_nbr)
        self._name = ism8.get_name(dp_nbr)
        self._type = ism8.get_type(dp_nbr)
        self._option_ids = {}
        self._ism8: Ism8 = ism8
        _LOGGER.debug("Setup select sensor no. %d as %s", self.dp_nbr, self._type)

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return (self._device + "_" + self._name).lower().replace(" ", "_")

    @property
    def unique_id(self) -> str:
        """Return the unique_id of this sensor."""
        return "wolf." + self._device.lower().replace(" ", "") + "." + str(self.dp_nbr)

    @property
    def options(self) -> list[str]:
        """Return all available options"""

        _options = []
        if self._type == "DPT_HVACContrMode":

            self._option_ids = self._ism8.HVACContrModes
        elif self._type == "DPT_HVACMode":

            self._option_ids = self._ism8.HVACModes
        elif self._type == "DPT_DHWMode":

            self._option_ids = self._ism8.DHWModes
        else:

            _LOGGER.error("Unknown datapoint type %s for select sensor", self._type)
        for key in self._option_ids:

            _options.append(self._option_ids[key])
        return _options

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

    async def async_update(self) -> None:
        """Return state"""
        self._attr_current_option = self._ism8.read(self.dp_nbr)
        return

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        for key in self._option_ids:
            if self._option_ids[key] == option:
                # self._ism8.send_dp_value(self.dp_nbr, key)
                _LOGGER.debug("self._ism8.send_dp_value(%d, %d)", self.dp_nbr, key)
