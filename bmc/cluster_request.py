"""Module to handle requests to the Turing Pi BMC."""
from ipaddress import IPv4Address

import requests

from bmc.exceptions import RequestException


class ClusterRequest:
    """Class to handle requests to the cluster."""

    __slots__ = ("_cluster_ip",)

    def __init__(self, cluster_ip: IPv4Address):
        """
        Initialise ClusterRequest.

        Args:
            cluster_ip: IP for the cluster
        """
        self._cluster_ip = cluster_ip

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
        full_url = f"http://{self._cluster_ip}/api/{url}"
        req = requests.post(url=full_url)
        if req.status_code != 200:
            raise RequestException("Non 200 response received")
        try:
            response = req.json()["response"][0]
        except (IndexError, KeyError):
            raise RequestException("Invalid response received")
        return response
