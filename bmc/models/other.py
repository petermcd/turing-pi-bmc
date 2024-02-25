"""About model."""

from datetime import datetime
from ipaddress import IPv4Address


class Other:
    """
    Other model.

    Attributes:
        _api: The API version.
        _build_version: The build version.
        _buildroot: The build root.
        _buildtime: The build time.
        _ip: The IP address.
        _mac: The MAC address.
        _version: The BMC version.
    """

    __slots__ = (
        "_api",
        "_build_version",
        "_buildroot",
        "_buildtime",
        "_ip",
        "_mac",
        "_version",
    )

    def __init__(self, data) -> None:
        """
        Other initializer.

        Args:
            data: A dictionary containing the response from the BMC.
        """
        try:
            self._api = data["api"]
            self._build_version = data["build_version"]
            self._buildroot = data["buildroot"]
            self._buildtime = datetime.fromisoformat(data["buildtime"])
            self._ip = IPv4Address(data["ip"])
            self._mac = data["mac"]
            self._version = data["version"]
        except KeyError as exc:
            raise ValueError(f"Invalid response, missing key {exc}") from exc

    @property
    def api(self) -> str:
        """
        Property for api.

        Returns:
            api as a string.
        """
        return self._api

    @property
    def build_version(self) -> str:
        """
        Property for build_version.

        Returns:
            build_version as a string.
        """
        return self._build_version

    @property
    def buildroot(self) -> str:
        """
        Property for buildroot.

        Returns:
            buildroot as a string.
        """
        return self._buildroot

    @property
    def buildtime(self) -> datetime:
        """
        Property for buildtime.

        Returns:
            buildtime as a datetime object.
        """
        return self._buildtime

    @property
    def ip(self) -> IPv4Address:
        """
        Property for ip.

        Returns:
            ip as an IPv4Address object.
        """
        return self._ip

    @property
    def mac(self) -> str:
        """
        Property for mac.

        Returns:
            mac as a string.
        """
        return self._mac

    @property
    def version(self) -> str:
        """
        Property for version.

        Returns:
            version as a string.
        """
        return self._version
