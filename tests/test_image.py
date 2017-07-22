"""Test image functions."""
import pathlib
import unittest

from pywal import wal


DEVNULL = pathlib.Path("/dev/null")


class TestImage(unittest.TestCase):
    """Test image functions."""
    def test_get_img(self):
        """> Validate image file."""
        result = wal.get_image("tests/test_files/test.jpg", DEVNULL)
        self.assertEqual(result, "tests/test_files/test.jpg")

    def test_get_img_dir(self):
        """> Validate image directory."""
        result = wal.get_image("tests/test_files", DEVNULL)
        self.assertEqual(result, "tests/test_files/test.jpg")


if __name__ == "__main__":
    unittest.main()
