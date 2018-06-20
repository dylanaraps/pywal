"""Test sequence functions."""
import unittest
import platform

from pywal import sequences
from pywal import util

# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class Testsequences(unittest.TestCase):
    """Test the sequence functions."""

    def test_set_special(self):
        """> Create special escape sequence."""
        alpha = "100"
        result = sequences.set_special(11,
                                       COLORS["special"]["background"],
                                       "h", alpha)

        if platform.uname()[0] == "Darwin":
            self.assertEqual(result, "\033]Ph1F211E\033\\")
        else:
            self.assertEqual(result, "\033]11;#1F211E\033\\")

    def test_set_special_alpha(self):
        """> Create special escape sequence with alpha."""
        alpha = "99"
        result = sequences.set_special(11,
                                       COLORS["special"]["background"],
                                       "h", alpha)

        if platform.uname()[0] == "Darwin":
            self.assertEqual(result, "\033]Ph1F211E\033\\")
        else:
            self.assertEqual(result, "\033]11;[99]#1F211E\033\\")

    def test_set_color(self):
        """> Create color escape sequence."""
        result = sequences.set_color(11, COLORS["colors"]["color0"])

        if platform.uname()[0] == "Darwin":
            self.assertEqual(result, "\033]Pb1F211E\033\\")
        else:
            self.assertEqual(result, "\033]4;11;#1F211E\033\\")

    def test_set_iterm_tab_color(self):
        """> Create iterm tab color sequences"""
        result = sequences.set_iterm_tab_color(COLORS["special"]["background"])
        self.assertEqual(len(result), 84)


if __name__ == "__main__":
    unittest.main()
