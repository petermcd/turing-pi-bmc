"""Class to interact with the management API of the Turing Pi 2."""
from ipaddress import IPv4Address
from typing import Optional
from xml.etree import ElementTree

import requests
import semver
import urllib3

from bmc.exceptions import RequestException
from bmc.models.about import About
from bmc.models.info import Info
from bmc.models.node import Node
from bmc.models.other import Other
from bmc.models.storage_details import StorageDetails
from bmc.models.usb_mode import USBMode
from bmc.session import Session
from bmc.turing_pi_types import TuringPiMode

urllib3.disable_warnings()


class Cluster:
    """
    Class to interact with the management API of the Turing Pi 2.

    Attributes:
        _about: About object.
        _info: Info object.
        _latest_version: Latest version of BMC from GitHub.
        _nodes: List of Nodes.
        _other: Other object.
        _session: Session object.
    """

    __slots__ = (
        "_about",
        "_info",
        "_latest_version",
        "_nodes",
        "_other",
        "_session",
    )

    def __init__(
        self, cluster_ip: IPv4Address, username: str, password: str, verify: bool = True
    ) -> None:
        """
        Initialize Cluster.

        Args:
            cluster_ip: Instance of IPv4Address representing the Ip of the Turing Pi board.
            username: Username for the Turing Pi board.
            password: Password for the Turing Pi board.
            verify: Verify the SSL certificate.
        """
        self._about: Optional[About] = None
        self._info: Optional[Info] = None
        self._latest_version: str = ""
        self._nodes: list[Node] = []
        self._other: Optional[Other] = None
        self._session: Session = Session(
            cluster_ip=cluster_ip, username=username, password=password, verify=verify
        )

    def about(self) -> About:
        """
        Fetch about details from the cluster.

        Returns:
            About object.
        """
        if not self._about:
            url = "bmc?opt=get&type=about"
            self._about = About(data=self._session.make_request(url=url)["result"])
        return self._about

    def info(self) -> Info:
        """
        Fetch about details from the cluster.

        Returns:
            About object.
        """
        if not self._info:
            url = "bmc?opt=get&type=info"
            self._info = Info(data=self._session.make_request(url=url)["result"])
        return self._info

    def get_usb_mode(self) -> USBMode:
        """
        Get USB mode.

        Returns:
            USBMode with mode and node values.
        """
        if not self._nodes:
            self.fetch_power()
        url = "bmc?opt=get&type=usb"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return USBMode(
                node=self._nodes[0],
                mode=TuringPiMode.Host,
            )
        node_name = int(response["result"][0]["node"].replace("Node ", "")) - 1
        return USBMode(
            node=self._nodes[node_name],
            mode=TuringPiMode(response["result"][0]["mode"]),
        )

    def latest_version(self) -> str:
        """
        Fetch the latest available version of BMC from GitHub.

        Returns:
            Latest version as a string.
        """
        if not self._latest_version:
            url: str = "https://github.com/turing-machines/BMC-Firmware/releases.atom"
            try:
                response = requests.get(url=url)
            except RequestException:
                return ""
            root = ElementTree.fromstring(response.text)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            latest_entry = entries[0]
            if latest_version := latest_entry.findall(
                "{http://www.w3.org/2005/Atom}title"
            )[0].text:
                self._latest_version = latest_version[1:]
            else:
                return ""
        return self._latest_version

    def other(self) -> Other:
        """Fetch data from the other info api."""
        if not self._other:
            url = "bmc?opt=get&type=other"
            self._other = Other(data=self._session.make_request(url=url)["result"][0])
        return self._other

    def fetch_power(self) -> bool:
        """
        Fetch power status of the nodes.

        Returns:
            True on success otherwise False.
        """
        url = "bmc?opt=get&type=power"

        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        for slot_id, node_name in enumerate(response["result"][0]):
            if slot_id not in self._nodes:
                self._nodes.append(
                    Node(
                        session=self._session,
                        slot=slot_id,
                        name=node_name,
                        description="",
                    )
                )
            self._nodes[slot_id].powered_on = response["result"][0][node_name] == "1"
        return True

    def network(self) -> bool:
        """
        Reset the Turing Pi 2 network.

        Return:
            True on success otherwise False.
        """
        url = "bmc?opt=set&type=network"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        return response["result"].lower() == "ok"

    @property
    def nodes(self) -> list[Node]:
        """
        Property for Nodes.

        Returns:
            List of Nodes.
        """
        if not self._nodes:
            self.fetch_power()
        return self._nodes

    def reload(self) -> bool:
        """
        Reload the system management daemon.

        Return:
            True on success otherwise False.
        """
        url = "bmc?opt=set&type=reload"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        return response["result"].lower() == "ok"

    def reboot(self) -> bool:
        """
        Reboot the Turing Pi 2.

        Return:
            True on success otherwise False.
        """
        url = "bmc?opt=set&type=reboot"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        return response["result"].lower() == "ok"

    @staticmethod
    def restart_node(node: Node) -> bool:
        """
        Restart the given node/nodes.

        Args:
            node: List of nodes to restart.

        Returns:
            True on success otherwise False.
        """
        return node.restart()

    def sdcard(self) -> StorageDetails:
        """
        Get SDCard data.

        Returns:
            True on success otherwise False.
        """
        url = "bmc?opt=get&type=sdcard"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return StorageDetails(
                name="SD Card",
                free_bytes=0,
                total_bytes=0,
                used_bytes=0,
            )
        return StorageDetails(
            name="SD Card",
            free_bytes=response["result"][0]["free"],
            total_bytes=response["result"][0]["total"],
            used_bytes=response["result"][0]["use"],
        )

    def set_usb_mode(self, usbmode: USBMode) -> bool:
        """
        Set USB mode on a node.

        Args:
            usbmode: USBMode containing details for mode and node.

        Returns:
            True on success otherwise False.
        """
        url = f"bmc?opt=set&type=usb&mode={usbmode.mode.value}&node={usbmode.node.slot - 1}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        try:
            result = response["result"]
        except KeyError:
            return False
        return result == "ok"

    def start_nodes(self, nodes: list[Node]) -> bool:
        """
        Start the given node/nodes.

        Args:
            nodes: List of nodes to start.

        Returns:
            True on success otherwise False.
        """
        node_list = "".join(f"&{node.name}=1" for node in nodes)
        url = f"bmc?opt=set&type=power{node_list}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        if response["result"].lower() == "ok":
            for node_item in nodes:
                node_item.powered_on = True
            return True
        return False

    def stop_nodes(self, nodes: list[Node]) -> bool:
        """
        Stop the given node/nodes.

        Args:
            nodes: List of nodes to stop.

        Returns:
            True on success otherwise False.
        """
        node_list = "".join(f"&{node.name}=0" for node in nodes)
        url = f"bmc?opt=set&type=power{node_list}"
        try:
            response = self._session.make_request(url=url)
        except RequestException:
            return False
        if response["result"].lower() == "ok":
            for node_item in nodes:
                node_item.powered_on = False
            return True
        return False

    def update_available(self) -> bool:
        """
        Check to see if a new version of BMC is available.

        Returns:
            True if update available otherwise False.
        """
        current_version: str = self.about().version
        latest_version: str = self.latest_version()
        return semver.compare(current_version, latest_version) < 0
