import unittest
from pathlib import Path

from vectorvfs.vfsstore import VFSStore, XAttrFile
import os
import tempfile


class TestVFSStore(unittest.TestCase):
    def setUp(self) -> None:
        self.root_path = Path(__file__).parent / "data"
        self.store = VFSStore(self.root_path)

    def test_search_text(self) -> None:
        pass


SKIP_XATTR = not all(hasattr(os, fn) for fn in (
    'listxattr', 'setxattr', 'getxattr', 'removexattr'
))

@unittest.skipIf(SKIP_XATTR, "xattr not supported on this platform")
class TestXAttrFile(unittest.TestCase):
    def setUp(self) -> None:
        # create a temporary file for xattr operations
        fd, path = tempfile.mkstemp()
        os.close(fd)
        self.file_path = Path(path)
        self.xfile = XAttrFile(self.file_path)

    def tearDown(self) -> None:
        try:
            self.file_path.unlink()
        except Exception:
            pass

    def test_list_empty(self):
        # no attributes initially
        self.assertEqual(self.xfile.list(), [])

    def test_write_and_read(self):
        key = 'user.test'
        data = b'hello world'
        self.xfile.write(key, data)
        names = self.xfile.list()
        self.assertIn(key, names)
        self.assertEqual(self.xfile.read(key), data)

    def test_overwrite(self):
        key = 'user.test'
        first = b'first'
        second = b'second'
        self.xfile.write(key, first)
        self.assertEqual(self.xfile.read(key), first)
        self.xfile.write(key, second)
        self.assertEqual(self.xfile.read(key), second)

    def test_remove(self):
        key = 'user.delete'
        data = b'todelete'
        self.xfile.write(key, data)
        self.assertIn(key, self.xfile.list())
        self.xfile.remove(key)
        self.assertNotIn(key, self.xfile.list())

    def test_read_nonexistent(self):
        with self.assertRaises(OSError):
            self.xfile.read('user.nothing')

    def test_remove_nonexistent(self):
        with self.assertRaises(OSError):
            self.xfile.remove('user.nothing')


if __name__ == "__main__":
    unittest.main()
