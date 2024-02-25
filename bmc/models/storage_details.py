"""StorageDetails model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StorageDetails:
    """
    StorageDetails model.

    Attributes:
        free_bytes: The number of free bytes.
        name: The name of the storage device.
        total_bytes: The total number of bytes.
        used_bytes: The number of used bytes.
    """

    __slots__ = (
        "_free_bytes",
        "_name",
        "_total_bytes",
        "_used_bytes",
    )

    def __init__(
        self,
        name: str,
        free_bytes: int,
        total_bytes: int,
        used_bytes: Optional[int] = None,
    ) -> None:
        """
        Storage Details initializer.

        Args:
            name: The name of the storage device.
            free_bytes: The number of free bytes.
            total_bytes: The total number of bytes.
            used_bytes: The number of used bytes.
        """
        self._free_bytes = free_bytes
        self._name = name
        self._total_bytes = total_bytes
        if used_bytes is None:
            self._used_bytes = total_bytes - free_bytes
        else:
            self._used_bytes = used_bytes

    @property
    def free_bytes(self) -> int:
        """
        Property for free_bytes.

        Returns:
            free_bytes as an int.
        """
        return self._free_bytes

    @property
    def name(self) -> str:
        """
        Property for name.

        Returns:
            name as a string.
        """
        return self._name

    @property
    def total_bytes(self) -> int:
        """
        Property for total_bytes.

        Returns:
            total_bytes as an int.
        """
        return self._total_bytes

    @property
    def used_bytes(self) -> int:
        """
        Property for used_bytes.

        Returns:
            used_bytes as an int.
        """
        return self._used_bytes
