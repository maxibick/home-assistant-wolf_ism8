"""
Support for Wolf heating via ISM8 adapter
"""
import logging
from homeassistant import config_entries
from pywolf8.ism8 import Ism8
from collections.abc import Callable
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
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
from homeassistant.const import (
    CONF_DEVICES,
    STATE_PROBLEM,
    STATE_OK,
    STATE_ON,
    STATE_OFF,
    STATE_UNKNOWN,
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

            if (
                ism8.get_type(nbr) == SensorType.DPT_SWITCH
                and nbr != 194
                and not (59 <= nbr <= 64)
                and not (72 <= nbr <= 77)
                and not (85 <= nbr <= 90)
                and not (98 <= nbr <= 103)
                and not (59 <= nbr <= 64)
                and not (152 <= nbr <= 150)
            ):
                sensors.append(WolfBinarySensor(ism8, nbr))
            elif ism8.get_type(nbr) == SensorType.DPT_BOOL:
                sensors.append(WolfBinarySensor(ism8, nbr))
            elif ism8.get_type(nbr) == SensorType.DPT_ENABLE:
                sensors.append(WolfBinarySensor(ism8, nbr))
            elif ism8.get_type(nbr) == SensorType.DPT_OPENCLOSE:
                sensors.append(WolfBinarySensor(ism8, nbr))

    async_add_entities(sensors)


class WolfBinarySensor(Entity):
    """Implementation of Wolf Heating System Sensor via ISM8-network adapter
    dp_nbr represents the unique identifier of the up to 200 different
    sensors
    """

    def __init__(self, ism8, dp_nbr):
        self.dp_nbr = dp_nbr
        self._device = ism8.get_device(dp_nbr)
        self._name = ism8.get_name(dp_nbr)
        self._type = ism8.get_type(dp_nbr)
        self._unit = ism8.get_unit(dp_nbr)
        self._state = STATE_UNKNOWN
        self._ism8 = ism8
        _LOGGER.debug("setup Sensor no. %d as %s", self.dp_nbr, self._type)

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
    def state(self):
        """Return the state of the device."""
        if self.device_class == BinarySensorDeviceClass.PROBLEM:
            return STATE_PROBLEM if self.is_on else STATE_OK
        else:
            return STATE_ON if self.is_on else STATE_OFF

    @property
    def is_on(self) -> str:
        """Return true if the binary sensor is on."""
        return self._state

    @property
    def device_class(self):
        """Return the class of the device."""
        if self._name == "Stoerung":
            return BinarySensorDeviceClass.PROBLEM
        elif self._name in ["Status Brenner / Flamme", "Status E-Heizung"]:
            return BinarySensorDeviceClass.HEAT
        elif self._name in [
            "Status Heizkreispumpe",
            "Status Speicherladepumpe",
            "Status Mischerkreispumpe",
            "Status Solarkreispumpe SKP1",
            "Status Zubringer-/Heizkreispumpe",
        ]:
            return BinarySensorDeviceClass.MOVING
        else:
            return None

    async def async_update(self):
        """Return state"""
        self._state = self._ism8.read(self.dp_nbr)
        return
