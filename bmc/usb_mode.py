"""Module to hold USBMode."""
from dataclasses import dataclass

from bmc.node import Node
from bmc.turing_pi_types import TuringPiMode


@dataclass
class USBMode:
    """Dataclass for USB Mode."""

    node: Node
    mode: TuringPiMode
