import io
import os
from pathlib import Path

import torch


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
    def __init__(self, xattrfile: XAttrFile) -> None:
        self.xattrfile = xattrfile

    def _tensor_to_bytes(self, tensor: torch.Tensor) -> bytes:
        buffer = io.BytesIO()
        torch.save(tensor, buffer)
        return buffer.getvalue()
    
    def _bytes_to_tensor(self, b: bytes, map_location=None) -> torch.Tensor:
        buffer = io.BytesIO(b)
        return torch.load(buffer, map_location=map_location, weights_only=True)

    def write_tensor(self, tensor: torch.Tensor) -> int:
        btensor = self._tensor_to_bytes(tensor)
        self.xattrfile.write("user.vectorvfs", btensor)
        return len(btensor)

    def read_tensor(self) -> torch.Tensor:
        btensor = self.xattrfile.read("user.vectorvfs")
        tensor = self._bytes_to_tensor(btensor)
        return tensor
