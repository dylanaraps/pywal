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
        util.Color.alpha_num = 100
        result = sequences.set_special(11, COLORS["special"]["background"])
        self.assertEqual(result, "\033]11;#1F211E\007")

    def test_set_special_alpha(self):
        """> Create special escape sequence with alpha."""
        util.Color.alpha_num = 99
        result = sequences.set_special(11, COLORS["special"]["background"])
        self.assertEqual(result, "\033]11;[99]#1F211E\007")

    def test_set_color(self):
        """> Create color escape sequence."""
        result = sequences.set_color(11, COLORS["colors"]["color0"])
        self.assertEqual(result, "\033]4;11;#1F211E\007")

    def test_set_iterm_tab_color(self):
        """> Create iterm tab color sequences"""
        result = sequences.set_iterm_tab_color(COLORS["special"]["background"])
        self.assertEqual(len(result), 104)

    def test_sequence_order(self):
        """> Test that the sequences are in order."""
        result = sequences.create_sequences(COLORS, vte=False).split("\007")
        self.assertEqual(result[2], "\x1b]4;2;#CC6A93")
        self.assertEqual(result[15], "\x1b]4;15;#F5F1F4")
        self.assertEqual(result[8], "\x1b]4;8;#666666")


if __name__ == "__main__":
    unittest.main()
