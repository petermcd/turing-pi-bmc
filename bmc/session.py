"""Session to the cluster."""

from ipaddress import IPv4Address
from typing import Any

import requests

from bmc.exceptions import RequestException


class Session:
    """
    Session to the cluster.

    Attributes:
        _cluster_ip: The IP address of the cluster.
        _session: The session to the cluster.
    """

    __slots__ = (
        "_cluster_ip",
        "_session",
    )

    def __init__(
        self, cluster_ip: IPv4Address, username: str, password: str, verify: bool = True
    ) -> None:
        """
        Create a session to the cluster.

        Args:
            cluster_ip: The IP address of the cluster.
            username: The username to use for the session.
            password: The password to use for the session.
            verify: Whether to verify the certificate of the cluster.
        """
        self._cluster_ip = cluster_ip
        self._session = requests.Session()
        self._session.verify = verify
        self._session.auth = (username, password)

    def make_request(self, url: str) -> Any:
        """
        Make a request to the cluster using the API.

        Args:
            url: The url for the request.

        Raises:
            RequestException: On incorrect response code or invalid response.

        Returns:
            Response from the request.
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
