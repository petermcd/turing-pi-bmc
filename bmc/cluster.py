"""Module to hold Cluster."""
from ipaddress import IPv4Address
from xml.etree import ElementTree

import requests
import semver

from bmc.cluster_request import ClusterRequest
from bmc.exceptions import RequestException
from bmc.node import Node
from bmc.sdcard import SDCard
from bmc.turing_pi_types import TuringPiMode
from bmc.usb_mode import USBMode


class Cluster:
    """Class to interact with the management API of the Turing Pi 2."""

    __slots__ = (
        "_cr",
        "_latest_version",
        "_installed_version",
        "_mac_address",
        "_nodes",
    )

    def __init__(self, cluster_ip: IPv4Address):
        """
        Initialise Cluster.

        Args:
            cluster_ip: Instance of IPv4Address representing the Ip of the Turing Pi board.
        """
        self._cr = ClusterRequest(cluster_ip=cluster_ip)
        self._installed_version: str = ""
        self._latest_version: str = ""
        self._mac_address: str = ""
        self._nodes: list[Node] = []
        self.fetch_nodes()

    def fetch_nodes(self):
        """
        Fetch nodes details from the cluster.

        List of Nodes:
        """
        self._nodes = []
        url = "bmc?opt=get&type=nodeinfo"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return False
        for slot_id, node_name in enumerate(response):
            # We add 1 to the slot_id as Turing Pi references slot 0 as slot 1
            current_node = Node(
                slot=slot_id + 1,
                name=node_name,
                description=response[node_name],
                cr=self._cr,
            )
            self._nodes.append(current_node)

    def fetch_power(self):
        """
        Fetch nodes details from the cluster.

        List of Nodes:
        """
        url = "bmc?opt=get&type=power"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return False
        for slot_id, node_name in enumerate(response):
            self._nodes[slot_id].powered_on = bool(response[node_name])

    def get_sdcard(self) -> SDCard:
        """
        Get SDCard data.

        Returns:
            True on success otherwise False
        """
        url = "bmc?opt=get&type=sdcard"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return SDCard(
                free=0,
                used=0,
                total=0,
            )
        return SDCard(
            free=response["free"],
            used=response["use"],
            total=response["total"],
        )

    def get_usb_mode(self) -> USBMode:
        """
        Get USB mode.

        Returns:
            USBMode with mode and node values
        """
        url = "bmc?opt=get&type=usb"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return USBMode(
                node=self._nodes[0],
                mode=TuringPiMode.Host,
            )

        return USBMode(
            node=self._nodes[response["node"]],
            mode=TuringPiMode(response["mode"]),
        )

    def reset_network(self) -> bool:
        """
        Reset the Turing Pi 2 network.

        Return:
            True on success otherwise False
        """
        url = "bmc?opt=set&type=network&cmd=reset"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return False
        return response.lower() == "ok"

    def set_usb_mode(self, usbmode: USBMode):
        """
        Set USB mode on a node.

        Args:
            usbmode: USBMode containing details for mode and node

        Returns:
            True on success otherwise False
        """
        url = (
            f"bmc?opt=set&type=usb&mode={usbmode.mode.value}&node={usbmode.node.slot-1}"
        )
        try:
            response = self._cr.make_request(url=url)
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
            nodes: List of nodes to start

        Returns:
            True on success otherwise False
        """
        node_list = "".join(f"&{node.name}=1" for node in nodes)
        url = f"bmc?opt=set&type=power{node_list}"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return False
        if response.lower() == "ok":
            for node_item in nodes:
                node_item.powered_on = True
            return True
        return False

    def stop_nodes(self, nodes: list[Node]) -> bool:
        """
        Stop the given node/nodes.

        Args:
            nodes: List of nodes to stop

        Returns:
            True on success otherwise False
        """
        node_list = "".join(f"&{node.name}=0" for node in nodes)
        url = f"bmc?opt=set&type=power{node_list}"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return False
        if response.lower() == "ok":
            for node_item in nodes:
                node_item.powered_on = False
            return True
        return False

    def update(self, file: str) -> bool:
        """
        Update the firmware using over the air.

        Args:
            file: Path to the file to upload

        Return:
            True on success otherwise False
        """
        # TODO implement
        return False

    @property
    def installed_version(self) -> str:
        """
        Fetch the installed version from the cluster.

        Returns:
            Latest version as a string.
        """
        if not self._installed_version:
            self._fetch_other_node_info()
        return self._installed_version

    @property
    def latest_version(self) -> str:
        """
        Fetch the latest available version of BMC from Github.

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
            latest_version = latest_entry.findall("{http://www.w3.org/2005/Atom}title")[
                0
            ].text
            if not latest_version:
                return ""
            self._latest_version = latest_version[1:]
        return self._latest_version

    @property
    def mac_address(self) -> str:
        """
        Fetch the cluster mac address.

        Returns:
            Cluster mac address.
        """
        if not self._mac_address:
            self._fetch_other_node_info()
        return self._mac_address

    @property
    def nodes(self) -> list[Node]:
        """
        Property for Nodes.

        List of Nodes.
        """
        return self._nodes

    @property
    def update_available(self) -> bool:
        """
        Check to see if a new version of BMC is available.

        Returns:
            True if update available otherwise False.
        """
        current_version: str = self.installed_version
        latest_version: str = self.latest_version
        return semver.compare(current_version, latest_version) < 0

    def _fetch_other_node_info(self):
        """Fetch data from the other info api."""
        url = "bmc?opt=get&type=other"
        try:
            response = self._cr.make_request(url=url)
        except RequestException:
            return ""
        if "version" in response:
            self._installed_version = response["version"]
        if "mac" in response:
            self._mac_address = response["mac"]
