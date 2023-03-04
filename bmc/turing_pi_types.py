"""Module to hold enums."""
from enum import Enum


class PowerStatus(Enum):
    """Enum for available node power status."""

    Off = 0
    On = 1


class TuringPiMode(Enum):
    """Enum for available node modes."""

    Host = 0
    Device = 1
