"""Info model."""

from ipaddress import IPv4Address

from bmc.models.interface_details import InterfaceDetails
from bmc.models.storage_details import StorageDetails


class Info:
    """
    Info model.

    Attributes:
        _interface: The IP details.
        _storage: The storage details.
    """

    __slots__ = (
        "_interface",
        "_storage",
    )

    def __init__(self, data) -> None:
        """
        Info initializer.

        Args:
            data: A dictionary containing the response from the BMC.
        """
        self._interface: list[InterfaceDetails] = []
        self._storage: list[StorageDetails] = []
        self._interface.extend(
            InterfaceDetails(
                device=ip_details["device"],
                ip=IPv4Address(ip_details["ip"]),
                mac=ip_details["mac"].strip(),
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

    @property
    def interface(self) -> list[InterfaceDetails]:
        """Return the interface details."""
        return self._interface

    @property
    def storage(self) -> list[StorageDetails]:
        """Return the storage details."""
        return self._storage
