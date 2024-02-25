"""Module to hold enums."""

from enum import Enum


class PowerStatus(Enum):
    """Enum for available node power status."""

    Off = 0
    On = 1


class TuringPiMode(Enum):
    """Enum for available Turing Pi modes."""

    host = "host"
    device = "device"


class TuringPiRoute(Enum):
    """Enum for available Turing Pi modes."""

    bmc = "bmc"
    usb_a = "usba"


class TuringPiMode2(Enum):
    """Enum for available Turing Pi modes as used in the set usb mode api call."""

    host_usb_a = 0
    device_usb_a = 1
    flash_host_usb_a = 2
    flash_device_usb_a = 3
    host_bmc = 4
    device_bmc = 5
    flash_host_bmc = 6
    flash_device_bmc = 7
