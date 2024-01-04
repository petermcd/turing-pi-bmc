"""Module to hold Node."""


class Node:
    """Class to manage Nodes."""

    __slots__ = (
        "_description",
        "_name",
        "_power",
        "_slot",
    )

    def __init__(self, slot: int, name: str, description: str):
        """
        Initialize Node.

        Args:
            slot: Slot number.
            name: Node name given by the cluster.
            description: Description provided by the cluster.
        """
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

    def flash(self, file_path: str) -> bool:
        """
        Flash the given file to the node.

        Args:
            file_path: Path to the file to flash

        Raises:
            NotImplementedError: Functionality not created yet.
        """
        raise NotImplementedError

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
