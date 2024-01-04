"""Module to hold Cluster."""
from ipaddress import IPv4Address
from xml.etree import ElementTree

import requests
import semver
import urllib3

from bmc.exceptions import RequestException
from bmc.node import Node
from bmc.sdcard import SDCard
from bmc.turing_pi_types import TuringPiMode
from bmc.usb_mode import USBMode

urllib3.disable_warnings()


class Cluster:
    """Class to interact with the management API of the Turing Pi 2."""

    __slots__ = (
        "_cluster_ip",
        "_latest_version",
        "_installed_version",
        "_mac_address",
        "_nodes",
        "_session",
    )

    def __init__(
        self, cluster_ip: IPv4Address, username: str, password: str, verify: bool = True
    ):
        """
        Initialize Cluster.

        Args:
            cluster_ip: Instance of IPv4Address representing the Ip of the Turing Pi board.
            username: Username for the Turing Pi board.
            password: Password for the Turing Pi board.
            verify: Verify the SSL certificate.
        """
        self._cluster_ip = cluster_ip
        self._session = requests.Session()
        self._session.verify = verify
        self._session.auth = (username, password)
        self._installed_version: str = ""
        self._latest_version: str = ""
        self._mac_address: str = ""
        self._nodes: list[Node] = []

    def fetch_power(self):
        """
        Fetch nodes details from the cluster.

        List of Nodes:
        """
        url = "bmc?opt=get&type=power"

        try:
            response = self.make_request(url=url)
        except RequestException:
            return False
        for slot_id, node_name in enumerate(response["result"][0]):
            if slot_id not in self._nodes:
                self._nodes.append(
                    Node(
                        slot=slot_id,
                        name=node_name,
                        description="",
                    )
                )
            self._nodes[slot_id].powered_on = response["result"][0][node_name] == "1"

    def get_sdcard(self) -> SDCard:
        """
        Get SDCard data.

        Returns:
            True on success otherwise False
        """
        url = "bmc?opt=get&type=sdcard"
        try:
            response = self.make_request(url=url)
        except RequestException:
            return SDCard(
                free=0,
                used=0,
                total=0,
            )
        return SDCard(
            free=response["result"][0]["free"],
            used=response["result"][0]["use"],
            total=response["result"][0]["total"],
        )

    def get_usb_mode(self) -> USBMode:
        """
        Get USB mode.

        Returns:
            USBMode with mode and node values
        """
        if not self._nodes:
            self.fetch_power()
        url = "bmc?opt=get&type=usb"
        try:
            response = self.make_request(url=url)
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

    def make_request(self, url: str):
        """
        Make a request to the cluster using the API.

        Args:
            url: The url for the request

        Raises:
            RequestException: On incorrect response code or invalid response

        Returns:
            Response from the request
        """
        full_url = f"https://{self._cluster_ip}/api/{url}"
        req = self._session.get(url=full_url)
        if req.status_code != 200:
            raise RequestException("Non 200 response received")
        try:
            response = req.json()["response"][0]
        except (IndexError, KeyError) as exc:
            raise RequestException("Invalid response received") from exc
        return response

    def reset_network(self) -> bool:
        """
        Reset the Turing Pi 2 network.

        Return:
            True on success otherwise False
        """
        url = "bmc?opt=set&type=network&cmd=reset"
        try:
            response = self.make_request(url=url)
        except RequestException:
            return False
        return response["result"].lower() == "ok"

    def set_usb_mode(self, usbmode: USBMode):
        """
        Set USB mode on a node.

        Args:
            usbmode: USBMode containing details for mode and node

        Returns:
            True on success otherwise False
        """
        url = f"bmc?opt=set&type=usb&mode={usbmode.mode.value}&node={usbmode.node.slot - 1}"
        try:
            response = self.make_request(url=url)
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
            response = self.make_request(url=url)
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
            nodes: List of nodes to stop

        Returns:
            True on success otherwise False
        """
        node_list = "".join(f"&{node.name}=0" for node in nodes)
        url = f"bmc?opt=set&type=power{node_list}"
        try:
            response = self.make_request(url=url)
        except RequestException:
            return False
        if response["result"].lower() == "ok":
            for node_item in nodes:
                node_item.powered_on = False
            return True
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
        if not self._nodes:
            self.fetch_power()
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
            response = self.make_request(url=url)
        except RequestException:
            return ""
        if "version" in response["result"][0]:
            self._installed_version = response["result"][0]["version"]
        if "mac" in response["result"][0]:
            self._mac_address = response["result"][0]["mac"]
