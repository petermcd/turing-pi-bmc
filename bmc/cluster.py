from ipaddress import IPv4Address
import requests

from bmc.node import Node
from bmc.exceptions import RequestException


class Cluster(object):
    """Class to interact with the management API of the Turing Pi 2."""
    __slots__ = (
        '_ip',
        '_nodes',
    )

    def __init__(self, ip: IPv4Address):
        """
        Initialise Cluster.

        Args:
            ip: Instance of IPv4Address representing the Ip of the Turing Pi board.
        """
        self._ip = ip
        self._nodes = list()
        self.fetch_nodes()

    def fetch_nodes(self):
        """
        Fetch nodes details from the cluster.

        List of Nodes:
        """
        self._nodes = list()
        url = 'bmc?opt=get&type=nodeinfo'
        try:
            response = self._make_request(url)
        except RequestException:
            return False
        for slot_id, node_name in enumerate(response):
            # We add 1 to the slot_id as Turing Pi references slot 0 as slot 1
            current_node = Node(slot=slot_id+1, name=node_name, description=response[node_name], cluster_ip=self._ip)
            self._nodes.append(current_node)

    def reset_network(self) -> bool:
        """
        Reset the Turing Pi 2 network.

        Return:
            True on success otherwise False
        """
        url = 'bmc?opt=set&type=network&cmd=reset'
        try:
            response = self._make_request(url)
        except RequestException:
            return False
        if response.lower() == 'ok':
            return True
        return False

    def start_nodes(self, nodes: list[Node]) -> bool:
        """
        Start the given node/nodes.

        Args:
            nodes: List of nodes to start

        Returns:
            True on success otherwise False
        """
        node_list = ''
        for node in nodes:
            node_list += f'&{node.name}=1'
        url = f'bmc?opt=set&type=power{node_list}'
        try:
            response = self._make_request(url)
        except RequestException:
            return False
        if response.lower() == 'ok':
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
        node_list = ''
        for node in nodes:
            node_list += f'&{node.name}=0'
        url = f'bmc?opt=set&type=power{node_list}'
        try:
            response = self._make_request(url)
        except RequestException:
            return False
        if response.lower() == 'ok':
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
    def nodes(self) -> list[Node]:
        """
        Property for Nodes.

        List of Nodes.
        """
        return self._nodes

    def _make_request(self, url: str):
        """
        Make a request to the cluster

        Args:
            url: The url for the request

        Raises:
            RequestException: On incorrect response code or invalid response

        Returns:
            Response from the request
        """
        full_url = f'http://{self._ip}/api/{url}'
        req = requests.post(url=full_url)
        if req.status_code != 200:
            raise RequestException('Non 200 response received')
        try:
            response = req.json()['response'][0]
        except:
            raise RequestException('Invalid response received')
        return response

ip = IPv4Address('192.168.1.175')
c = Cluster(ip=ip)
c.stop_nodes(c.nodes)
