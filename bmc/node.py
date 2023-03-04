import requests
from ipaddress import IPv4Address

from bmc.exceptions import RequestException


class Node(object):
    """Class to manage Nodes."""
    __slots__ = (
        '_cluster_ip',
        '_description',
        '_name',
        '_slot',
    )

    def __init__(self, slot: int, name: str, description: str, cluster_ip: IPv4Address):
        """
        Initialise Node.

        Args:
            slot: Slot number
            name: Node name given by the cluster
            description: Description provided by the cluster
            cluster_ip
        """
        self._cluster_ip = cluster_ip
        self._description = description
        self._name = name
        self._slot = slot

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
        url = f'bmc?opt=set&type=power&{self.name}=1'
        try:
            response = self._make_request(url)
        except RequestException:
            return False
        if response.lower() == 'ok':
            return True
        return False

    def stop_nodes(self) -> bool:
        """
        Stop the given node/nodes.

        Returns:
            True on success otherwise False
        """
        url = f'bmc?opt=set&type=power&{self.name}=0'
        try:
            response = self._make_request(url)
        except RequestException:
            return False
        if response.lower() == 'ok':
            return True
        return False

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
        full_url = f'http://{self._cluster_ip}/api/{url}'
        req = requests.post(url=full_url)
        if req.status_code != 200:
            raise RequestException('Non 200 response received')
        try:
            response = req.json()['response'][0]
        except:
            raise RequestException('Invalid response received')
        return response
