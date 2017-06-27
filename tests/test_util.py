"""Test util functions."""
import unittest
import pathlib
from pywal import util


class TestUtil(unittest.TestCase):
    """Test the util functions."""

    def test_read_file_start(self):
        """Test read_file()."""
        result = util.read_file("tests/test_file")
        self.assertEqual(result[0], "#363442")

    def test_read_file_end(self):
        """Test read_file()."""
        result = util.read_file("tests/test_file")
        self.assertEqual(result[15], "#C9CFD0")

    def test_save_file(self):
        """Test save_file()."""
        tmp_file = pathlib.Path("/tmp/test_file")
        util.save_file("Hello, world", tmp_file)
        result = tmp_file.is_file()
        self.assertTrue(result)

    def test_create_dir(self):
        """Test create_dir()."""
        tmp_dir = pathlib.Path("/tmp/test_dir")
        util.create_dir(tmp_dir)
        result = tmp_dir.is_dir()
        self.assertTrue(result)

    def test_hex_to_rgb_black(self):
        """Test hex_to_rgb() on #000000."""
        result = util.hex_to_rgb("#000000")
        self.assertEqual(result, "0,0,0")

    def test_hex_to_rgb_white(self):
        """Test hex_to_rgb() on #FFFFFF."""
        result = util.hex_to_rgb("#FFFFFF")
        self.assertEqual(result, "255,255,255")

    def test_hex_to_rgb_rand(self):
        """Test hex_to_rgb() on #98AEC2."""
        result = util.hex_to_rgb("#98AEC2")
        self.assertEqual(result, "152,174,194")

    # Figure out how to test this.
    # def test_disown(self):


if __name__ == "__main__":
    unittest.main()
