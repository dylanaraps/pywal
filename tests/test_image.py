"""Test image functions."""
import pathlib
import unittest

from pywal import wal


CACHE_DIR = pathlib.Path("/tmp/wal")


class TestImage(unittest.TestCase):
    """Test image functions."""
    def test_get_img(self):
        """> Validate image file."""
        result = wal.get_image("tests/test_files/test.jpg", CACHE_DIR)
        self.assertEqual(result, "tests/test_files/test.jpg")

    def test_get_img_dir(self):
        """> Validate image directory."""
        result = wal.get_image("tests/test_files", CACHE_DIR)
        self.assertEqual(result, "tests/test_files/test2.jpg")


if __name__ == "__main__":
    unittest.main()
