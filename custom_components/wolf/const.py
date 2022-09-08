"""Constants for wolf ism8 integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "wolf"

WOLF_DEVICES: Final = [
    "HG1",
    "HG2",
    "HG3",
    "HG4",
    "BM1",
    "BM2",
    "BM3",
    "BM4",
    "KM",
    "MM1",
    "MM2",
    "MM3",
    "SM",
    "CWL",
    "BWL",
]
DEVICE_INFO: Final = {
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


DEFAULT_WOLF_DEVICE: Final = "HG1"
DEFAULT_PORT: Final = 12004
DEFAULT_HOST: Final = "0.0.0.0"
