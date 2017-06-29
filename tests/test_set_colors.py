"""Test set functions."""
import unittest

from pywal import set_colors
from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class TestSetColors(unittest.TestCase):
    """Test the set_colors functions."""

    def test_set_special(self):
        """> Create special escape sequence."""
        result = set_colors.set_special(11, COLORS["special"]["background"])
        self.assertEqual(result, "\x1b]11;#3A5130\x07")

    def test_set_color(self):
        """> Create color escape sequence."""
        result = set_colors.set_color(11, COLORS["colors"]["color0"])
        self.assertEqual(result, "\033]4;11;#3A5130\007")

    def test_set_grey(self):
        """> Create special escape sequence."""
        colors = [list(COLORS["colors"].values())]
        result = set_colors.set_grey(colors[0])
        self.assertEqual(result, "#999999")


if __name__ == "__main__":
    unittest.main()
