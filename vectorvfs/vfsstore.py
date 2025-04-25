import os
from pathlib import Path


class XAttrFile:
    def __init__(self, file_path: Path) -> None:
        """
        Initialize an XAttrFile for managing extended attributes on a file.
        :param file_path: Path to the target file.
        """
        self.file_path = file_path

    def list(self) -> list[str]:
        """
        List all extended attribute names set on the file.
        :return: List of attribute names.
        """
        return os.listxattr(str(self.file_path))

    def write(self, key: str, data: bytes) -> None:
        """
        Write or replace an extended attribute on the file.
        :param key: Name of the attribute (e.g., 'user.comment').
        :param data: Bytes to store in the attribute.
        """
        os.setxattr(str(self.file_path), key, data)

    def read(self, key: str) -> bytes:
        """
        Read the value of an extended attribute from the file.
        :param key: Name of the attribute to read.
        :return: Bytes stored in the attribute.
        """
        return os.getxattr(str(self.file_path), key)

    def remove(self, key: str) -> None:
        """
        Remove an extended attribute from the file.
        :param key: Name of the attribute to remove.
        """
        os.removexattr(str(self.file_path), key)


class VFSStore:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

    def search_text(self, text: str) -> None:
        pass