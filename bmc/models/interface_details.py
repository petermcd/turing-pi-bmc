"""IPDetails model."""

from dataclasses import dataclass
from ipaddress import IPv4Address


@dataclass
class InterfaceDetails:
    """
    InterfaceDetails model.

    Attributes:
        _device: The device name.
        _ip: The IP address.
        _mac: The MAC address.
    """

    __slots__ = (
        "_device",
        "_ip",
        "_mac",
    )

    def __init__(self, device: str, ip: IPv4Address, mac: str) -> None:
        """
        IP details initializer.

        Args:
            device: The device name.
            ip: The IP address.
            mac: The MAC address.
        """
        self._device = device
        self._ip = ip
        self._mac = mac

    @property
    def device(self) -> str:
        """
        Property for device.

        Returns:
            device as a string.
        """
        return self._device

    @property
    def ip(self) -> IPv4Address:
        """
        Property for ip.

        Returns:
            ip as an IPv4Address.
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
