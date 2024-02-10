"""Module to hold enums."""
from enum import Enum


class PowerStatus(Enum):
    """Enum for available node power status."""

    Off = 0
    On = 1


class TuringPiMode(Enum):
    """
    Enum for available Turing Pi modes.

    Attributes:
        Host: Host mode.
        Device: Device mode.
    """

    Host = "Host"
    Device = "Device"


TuringPiMode2: dict[int, dict[str, str]] = {
    0: {
        "mode": "Host",
        "router": "USB-A",
    },
    1: {
        "mode": "Device",
        "router": "USB-A",
    },
    2: {
        "mode": "Flash (Host)",
        "router": "USB-A",
    },
    3: {
        "mode": "Flash (Device)",
        "router": "USB-A",
    },
    4: {
        "mode": "Host",
        "router": "BMC",
    },
    5: {
        "mode": "Device",
        "router": "BMC",
    },
    6: {
        "mode": "Flash (Host)",
        "router": "BMC",
    },
    7: {
        "mode": "Flash (Device)",
        "router": "BMC",
    },
}
