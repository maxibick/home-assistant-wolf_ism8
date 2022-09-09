"""
Support for Wolf heating via ISM8 adapter
"""

import logging
from homeassistant import config_entries
from collections.abc import Callable
from homeassistant.components.select import SelectEntity
from pywolf8.ism8 import Ism8
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

            if ism8.get_type(nbr) == SensorType.DPT_TEMPD:
                sensors.append(WolfSelect(ism8, nbr))
            elif ism8.get_type(nbr) in [
                SensorType.DPT_HVACMODE,
                SensorType.DPT_DHWMODE,
                SensorType.DPT_HVACCONTRMODE,
            ] and ism8.is_writable(nbr):
                sensors.append(WolfSelect(ism8, nbr))
            elif ism8.get_type(nbr) == SensorType.DPT_SWITCH and nbr in [
                59,
                62,
                72,
                75,
                85,
                88,
                98,
                101,
                150,
            ]:
                sensors.append(WolfProgrammSelect(ism8, nbr))

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
        _LOGGER.debug(
            "Setup select sensor %s (dd_id: %d) as %s",
            self._name,
            self.dp_nbr,
            self._type,
        )

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
    def options(self) -> list[str]:
        """Return all available options"""

        _options = []
        if self._type == SensorType.DPT_HVACCONTRMODE:

            for accaptable_option in self._ism8.get_value_area(self.dp_nbr):
                _options.append(self._ism8.HVACContrModes[accaptable_option])
        elif self._type == SensorType.DPT_HVACMODE:

            for accaptable_option in self._ism8.get_value_area(self.dp_nbr):
                _options.append(self._ism8.HVACModes[accaptable_option])
        elif self._type == SensorType.DPT_DHWMODE:

            for accaptable_option in self._ism8.get_value_area(self.dp_nbr):
                _options.append(self._ism8.DHWModes[accaptable_option])
        elif self._type == SensorType.DPT_TEMPD:

            for accaptable_option in self._ism8.get_value_area(self.dp_nbr):
                _options.append(str(accaptable_option))
        else:

            _LOGGER.error("Unknown datapoint type %s for select sensor", self._type)
        return _options

    async def async_update(self) -> None:
        """Return state"""
        self._attr_current_option = self._ism8.read(self.dp_nbr)
        return

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self._type == SensorType.DPT_TEMPD:
            option = float(option)
        self._ism8.send_dp_value(self.dp_nbr, option)


class WolfProgrammSelect(SelectEntity):
    """Implementation of Wolf Heating System Sensor via ISM8-network adapter
    dp_nbr represents the unique identifier of the up to 200 different
    sensors
    """

    _attr_current_option = None

    def __init__(self, ism8: Ism8, dp_nbr: int) -> None:
        self.dp_nbr = dp_nbr
        self._device = ism8.get_device(dp_nbr)
        self._name = ism8.get_name(dp_nbr)[:-2]
        for i in range(1, 3, 1):
            if ism8.get_name(dp_nbr + i)[:-2] != self._name:
                _LOGGER.error(
                    "Set up programm select %s failed with invalid datapoints", dp_nbr
                )
                break

        self._type = ism8.get_type(dp_nbr)
        self._ism8: Ism8 = ism8
        _LOGGER.debug(
            "Setup select sensor %s (dd_id: %d) as %s",
            self._name,
            self.dp_nbr,
            self._type,
        )

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
    def options(self) -> list[str]:
        """Return all available options"""
        return ["1", "2", "3"]

    async def async_update(self) -> None:
        """Return state"""
        _prog = "1"
        if self._ism8.read(self.dp_nbr):
            _prog = "1"
        elif self._ism8.read(self.dp_nbr + 1):
            _prog = "2"
        elif self._ism8.read(self.dp_nbr + 2):
            _prog = "3"
        self._attr_current_option = _prog
        return

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._ism8.send_dp_value(self.dp_nbr + (int(option) - 1), 1)
