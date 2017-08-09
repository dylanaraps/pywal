"""Test util functions."""
import unittest
import os

from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class TestUtil(unittest.TestCase):
    """Test the util functions."""

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
        tmp_file = "/tmp/test_file"
        util.save_file("Hello, world", tmp_file)
        result = os.path.isfile(tmp_file)
        self.assertTrue(result)

    def test_save_file_json(self):
        """> Save colors to a file."""
        tmp_file = "/tmp/test_file.json"
        util.save_file_json(COLORS, tmp_file)
        result = os.path.isfile(tmp_file)
        self.assertTrue(result)

    def test_create_dir(self):
        """> Create a directory."""
        tmp_dir = "/tmp/test_dir"
        util.create_dir(tmp_dir)
        self.assertTrue(os.path.isdir(tmp_dir))
        os.rmdir(tmp_dir)

    def test_hex_to_rgb_black(self):
        """> Convert #000000 to RGB."""
        result = util.hex_to_rgb("#000000")
        self.assertEqual(result, (0, 0, 0))

    def test_hex_to_rgb_white(self):
        """> Convert #ffffff to RGB."""
        result = util.hex_to_rgb("#ffffff")
        self.assertEqual(result, (255, 255, 255))

    def test_hex_to_rgb_rand(self):
        """> Convert #98aec2 to RGB."""
        result = util.hex_to_rgb("#98aec2")
        self.assertEqual(result, (152, 174, 194))

    def test_hex_to_xrgba(self):
        """> Convert #98aec2 to XRGBA."""
        result = util.hex_to_xrgba("#98aec2")
        self.assertEqual(result, "98/ae/c2/ff")

    def test_rgb_to_hex(self):
        """> Convert 152,174,194 to HEX."""
        result = util.rgb_to_hex((152, 174, 194))
        self.assertEqual(result, "#98aec2")

    def test_darken_color(self):
        """> Darken #ffffff by 0.25."""
        result = util.darken_color("#ffffff", 0.25)
        self.assertEqual(result, "#bfbfbf")

    def test_lighten_color(self):
        """> Lighten #000000 by 0.25."""
        result = util.lighten_color("#000000", 0.25)
        self.assertEqual(result, "#3f3f3f")


if __name__ == "__main__":
    unittest.main()
