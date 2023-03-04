"""Module to hold Node."""
from bmc.cluster_request import ClusterRequest
from bmc.exceptions import RequestException


class Node:
    """Class to manage Nodes."""

    __slots__ = (
        "_cr",
        "_description",
        "_name",
        "_power",
        "_slot",
    )

    def __init__(self, slot: int, name: str, description: str, cr: ClusterRequest):
        """
        Initialise Node.

        Args:
            slot: Slot number
            name: Node name given by the cluster
            description: Description provided by the cluster
            cr: ClusterRequest instance
        """
        self._cr = cr
        self._description = description
        self._name = name
        self._slot = slot
        self._power = False

    @property
    def description(self) -> str:
        """
        Property for node description.

        Returns:
            Node description as a string
        """
        return self._description

    @property
    def name(self) -> str:
        """
        Property for node name.

        Returns:
            Node name as a string
        """
        return self._name

    @property
    def slot(self) -> int:
        """
        Property for node slot.

        Returns:
            Node slot as an int
        """
        return self._slot

    def start_nodes(self) -> bool:
        """
        Start the node.

        Returns:
            True on success otherwise False
        """
        url = f"bmc?opt=set&type=power&{self.name}=1"
        try:
            response = self._cr.make_request(url)
        except RequestException:
            return False
        if response.lower() == "ok":
            self.powered_on = True
            return True
        return False

    def stop_nodes(self) -> bool:
        """
        Stop the given node/nodes.

        Returns:
            True on success otherwise False
        """
        url = f"bmc?opt=set&type=power&{self.name}=0"
        try:
            response = self._cr.make_request(url)
        except RequestException:
            return False
        if response.lower() == "ok":
            self.powered_on = False
            return True
        return False

    @property
    def powered_on(self) -> bool:
        """
        Identify if the node has power.

        Returns:
            True if powered on otherwise False
        """
        return self._power

    @powered_on.setter
    def powered_on(self, powered_on: bool):
        """
        Set if the node has power.

        Args:
            powered_on: True if powered on otherwise False
        """
        self._power = powered_on
