"""Info model."""
from ipaddress import IPv4Address

from bmc.models.ip_details import IPDetails
from bmc.models.storage_details import StorageDetails


class Info:
    """
    Info model.

    Attributes:
        _ip: The IP details.
        _storage: The storage details.
    """

    __slots__ = (
        "_ip",
        "_storage",
    )

    def __init__(self, data) -> None:
        """
        Info initializer.

        Args:
            data: A dictionary containing the response from the BMC.
        """
        self._ip: list[IPDetails] = []
        self._storage: list[StorageDetails] = []
        self._ip.extend(
            IPDetails(
                device=ip_details["device"],
                ip=IPv4Address(ip_details["ip"]),
                mac=ip_details["mac"],
            )
            for ip_details in data["ip"]
        )
        self._storage.extend(
            StorageDetails(
                name=storage_details["name"],
                free_bytes=storage_details["bytes_free"],
                total_bytes=storage_details["total_bytes"],
            )
            for storage_details in data["storage"]
        )
