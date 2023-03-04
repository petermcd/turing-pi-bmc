"""Module to hold SDCard."""
from dataclasses import dataclass


@dataclass
class SDCard:
    """Dataclass for SDCard data."""

    free: int
    total: int
    used: int
