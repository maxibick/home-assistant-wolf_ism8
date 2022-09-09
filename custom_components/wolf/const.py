"""Constants for wolf ism8 integration."""
from __future__ import annotations

from typing import Final

from homeassistant.backports.enum import StrEnum

DOMAIN: Final = "wolf"

DEFAULT_HOST: Final = "0.0.0.0"
DEFAULT_PORT: Final = 12004

WOLF_DEFAULT_DEVICES: Final = [
    "HG1",
    "BM1",
]
WOLF_DEVICES: Final = {
    "HG1": ("Heizgerät 1", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "HG2": ("Heizgerät 2 (In Kaskade)", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "HG3": ("Heizgerät 3 (In Kaskade)", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "HG4": ("Heizgerät 4 (In Kaskade)", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "BM1": (
        "Direkter Heizkreis + direktes Warmwasser",
        "Wolf",
        "TOB, CGB-2 oder MGK-2",
        "FW1.50",
    ),
    "BM2": ("Mischerkreis 1 + Warmwasser 1", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "BM3": ("Mischerkreis 2 + Warmwasser 2", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "BM4": ("Mischerkreis 3 + Warmwasser 3", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "KM": ("Kaskadenmodul", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "MM1": ("Mischermodul 1", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "MM2": ("Mischermodul 2", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "MM3": ("Mischermodul 3", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "SM": ("Solarmodul", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "CWL": ("CWL Excellent", "Wolf", "TOB, CGB-2 oder MGK-2", "FW1.50"),
    "BWL": ("Heizgerät 1", "Wolf", "BWL-1-S", "FW1.50"),
}
DEVICE_INFO_NAME: Final = 0
DEVICE_INFO_MANUFACTURER: Final = 1
DEVICE_INFO_MODELL: Final = 2
DEVICE_INFO_SW_VERSION: Final = 3


class SensorType(StrEnum):
    """Datapoint classes according to pywolf8 datapoint types"""

    DPT_SWITCH = "DPT_Switch"
    DPT_BOOL = "DPT_Bool"
    DPT_ENABLE = "DPT_Enable"
    DPT_OPENCLOSE = "DPT_OpenClose"
    DPT_SCALING = "DPT_Scaling"
    DPT_VALUE_TEMP = "DPT_Value_Temp"
    DPT_VALUE_TEMPD = "DPT_Value_Tempd"
    DPT_TEMPD = "DPT_Tempd"
    DPT_VALUE_PRES = "DPT_Value_Pres"
    DPT_POWER = "DPT_Power"
    DPT_VALUE_VOLUME_FLOW = "DPT_Value_Volume_Flow"
    DPT_TIMEOFDAY = "DPT_TimeOfDay"
    DPT_DATE = "DPT_Date"
    DPT_FLOWRATE_M3 = "DPT_FlowRate_m3/h"
    DPT_HVACMODE = "DPT_HVACMode"
    DPT_DHWMODE = "DPT_DHWMode"
    DPT_HVACCONTRMODE = "DPT_HVACContrMode"
