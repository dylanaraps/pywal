"""Test format functions."""
import unittest
from pywal import format_color
from pywal import util


# Import colors.
COLORS = util.read_file("tests/test_file")


class TestExportColors(unittest.TestCase):
    """Test the format_colors functions."""

    def test_plain(self):
        """> Convert colors to plain."""
        result = format_color.plain(COLORS)
        self.assertEqual(result[0], "#363442\n")

    def test_shell(self):
        """> Convert colors to shell variables."""
        result = format_color.shell(COLORS)
        self.assertEqual(result[0], "color0='#363442'\n")

    def test_css(self):
        """> Convert colors to css variables."""
        result = format_color.css(COLORS)
        self.assertEqual(result[1], "\t--color0: #363442;\n")

    def test_scss(self):
        """> Convert colors to scss variables."""
        result = format_color.scss(COLORS)
        self.assertEqual(result[0], "$color0: #363442;\n")

    def test_putty(self):
        """> Convert colors to putty theme."""
        result = format_color.putty(COLORS)
        self.assertEqual(result[2], "\"colour0\"=\"54,52,66\"\n")

    def test_xrdb(self):
        """> Convert colors to putty theme."""
        result = format_color.xrdb(COLORS)
        self.assertEqual(result[6], "*.color0: #363442\n*color0: #363442\n")


if __name__ == "__main__":
    unittest.main()
