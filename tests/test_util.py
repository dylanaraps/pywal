"""Test util functions."""
import unittest
import pathlib

from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class TestUtil(unittest.TestCase):
    """Test the util functions."""

    def test_set_grey(self):
        """> Get grey color based on brightness of color0"""
        colors = [list(COLORS["colors"].values())]
        result = util.set_grey(colors[0])
        self.assertEqual(result, "#666666")

    def test_read_file(self):
        """> Read colors from a file."""
        result = util.read_file("tests/test_files/test_file")
        self.assertEqual(result[0], "/home/dylan/Pictures/Wallpapers/1.jpg")

    def test_read_file_start(self):
        """> Read colors from a file."""
        result = util.read_file_json("tests/test_files/test_file.json")
        self.assertEqual(result["colors"]["color0"], "#1F211E")

    def test_read_file_end(self):
        """> Read colors from a file."""
        result = util.read_file_json("tests/test_files/test_file.json")
        self.assertEqual(result["colors"]["color15"], "#F5F1F4")

    def test_read_wallpaper(self):
        """> Read wallpaper from json file."""
        result = util.read_file_json("tests/test_files/test_file.json")
        self.assertEqual(result["wallpaper"], "5.png")

    def test_save_file(self):
        """> Save colors to a file."""
        tmp_file = pathlib.Path("/tmp/test_file")
        util.save_file("Hello, world", tmp_file)
        result = tmp_file.is_file()
        self.assertTrue(result)

    def test_save_file_json(self):
        """> Save colors to a file."""
        tmp_file = pathlib.Path("/tmp/test_file.json")
        util.save_file_json(COLORS, tmp_file)
        result = tmp_file.is_file()
        self.assertTrue(result)

    def test_create_dir(self):
        """> Create a directoru."""
        tmp_dir = pathlib.Path("/tmp/test_dir")
        util.create_dir(tmp_dir)
        result = tmp_dir.is_dir()
        self.assertTrue(result)

    def test_hex_to_rgb_black(self):
        """> Convert #000000 to RGB."""
        result = util.hex_to_rgb("#000000")
        self.assertEqual(result, "0,0,0")

    def test_hex_to_rgb_white(self):
        """> Convert #FFFFFF to RGB."""
        result = util.hex_to_rgb("#FFFFFF")
        self.assertEqual(result, "255,255,255")

    def test_hex_to_rgb_rand(self):
        """> Convert #98AEC2 to RGB."""
        result = util.hex_to_rgb("#98AEC2")
        self.assertEqual(result, "152,174,194")

    def test_hex_to_xrgba(self):
        """> Convert #98AEC2 to XRGBA."""
        result = util.hex_to_xrgba("#98AEC2")
        self.assertEqual(result, "98/ae/c2/ff")


if __name__ == "__main__":
    unittest.main()
