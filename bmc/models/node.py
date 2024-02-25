"""Class to handle the session with the BMC API."""

from bmc.exceptions import RequestException
from bmc.session import Session
from bmc.turing_pi_types import TuringPiMode2


class Node:
    """
    Node model.

    Attributes:
        _description: The node description.
        _name: The node name.
        _power: The node power state.
        _session: The session to use.
        _slot: The node slot.
    """

    __slots__ = (
        "_description",
        "_name",
        "_power",
        "_session",
        "_slot",
    )

    def __init__(
        self, session: Session, slot: int, name: str, description: str
    ) -> None:
        """
        Node initializer.

        Args:
            session: The session to use.
            slot: The slot number of the node.
            name: The name of the node.
            description: The description of the node.
        """
        self._description = description
        self._name = name
        self._session = session
        self._slot = slot
        self._power = False

    def __repr__(self) -> str:
        """
        Return string representation of Node.

        Returns:
            String representation of Node.
        """
        return f"Node(name={self._name}, slot={self._slot}, description={self._description})"

    def __str__(self) -> str:
        """
        Return string representation of Node.

        Returns:
            String representation of Node.
        """
        return self._name

    def clear_usb_boot(self) -> bool:
        """
        Clear USB Boot for the node.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=clear_usb_boot&node={self.slot - 1}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        try:
            result = response["result"]
        except KeyError:
            return False
        return result == "ok"

    @property
    def description(self) -> str:
        """
        Property for node description.

        Returns:
            Node description as a string.
        """
        return self._description

    @property
    def name(self) -> str:
        """
        Property for node name.

        Returns:
            Node name as a string.
        """
        return self._name

    @property
    def slot(self) -> int:
        """
        Property for node slot.

        Returns:
            Node slot as an int.
        """
        return self._slot

    @property
    def powered_on(self) -> bool:
        """
        Identify if the node has power.

        Returns:
            True if powered on otherwise False.
        """
        return self._power

    @powered_on.setter
    def powered_on(self, powered_on: bool) -> None:
        """
        Set if the node has power. This does not start/stop a node.

        Args:
            powered_on: True if powered on otherwise False.
        """
        self._power = powered_on

    def set_mass_storage_device(self) -> bool:
        """
        Set node as a mass storage devicee.

        Raises:
            RequestException: If there is an error making the request.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=node_to_msd&node={self._slot - 1}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        return response["result"].lower() == "ok"

    def set_usb_mode(self, usbmode: TuringPiMode2) -> bool:
        """
        Set USB mode on the node.

        Args:
            usbmode: USB mode from TuringPiMode2.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=usb&mode={usbmode.value}&node={self.slot - 1}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        try:
            result = response["result"]
        except KeyError:
            return False
        return result == "ok"

    def start(self) -> bool:
        """
        Start the node.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=power&{self._name}=1"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        if response["result"].lower() == "ok":
            self.powered_on = True
            return True
        return False

    def stop(self) -> bool:
        """
        Stop the node.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=power&{self._name}=0"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        if response["result"].lower() == "ok":
            self.powered_on = False
            return True
        return False

    def usb_boot(self) -> bool:
        """
        USB Boot the node.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=usb_boot&node={self.slot - 1}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        try:
            result = response["result"]
        except KeyError:
            return False
        return result == "ok"
