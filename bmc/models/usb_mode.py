"""USB Mode Model."""

from dataclasses import dataclass

from bmc.models.node import Node
from bmc.turing_pi_types import TuringPiMode, TuringPiRoute


@dataclass
class USBMode:
    """
    USB Mode Model.

    Attributes:
        node (Node): Node that the USB mode is set on.
        mode (TuringPiMode): USB mode that the node is set to.
    """

    node: Node
    mode: TuringPiMode
    route: TuringPiRoute
