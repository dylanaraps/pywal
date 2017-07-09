"""Test sequence functions."""
import unittest

from pywal import sequences
from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class Testsequences(unittest.TestCase):
    """Test the sequence functions."""

    def test_set_special(self):
        """> Create special escape sequence."""
        result = sequences.set_special(11, COLORS["special"]["background"])
        self.assertEqual(result, "\x1b]11;#1F211E\x07")

    def test_set_color(self):
        """> Create color escape sequence."""
        result = sequences.set_color(11, COLORS["colors"]["color0"])
        self.assertEqual(result, "\033]4;11;#1F211E\007")


if __name__ == "__main__":
    unittest.main()
