"""Test set functions."""
import unittest

from pywal import set_colors
from pywal import util


# Import colors.
COLORS = util.read_file("tests/test_files/test_file")


class TestSetColors(unittest.TestCase):
    """Test the set_colors functions."""

    def test_set_special(self):
        """> Create special escape sequence."""
        result = set_colors.set_special(11, COLORS[0])
        self.assertEqual(result, "\x1b]11;#363442\x07")

    def test_set_color(self):
        """> Create color escape sequence."""
        result = set_colors.set_color(11, COLORS[0])
        self.assertEqual(result, "\033]4;11;#363442\007")

    def test_set_grey(self):
        """> Create special escape sequence."""
        result = set_colors.set_grey(COLORS)
        self.assertEqual(result, "#999999")


if __name__ == "__main__":
    unittest.main()
