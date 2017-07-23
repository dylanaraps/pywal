"""Test sequence functions."""
import unittest
import unittest.mock
import io

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

    def test_send_sequences(self):
        """> Send sequences to all open terminals."""
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            sequences.send(COLORS, False)
            data = fake_out.getvalue().strip()
            self.assertTrue(data.endswith("colors: Set terminal colors"))


if __name__ == "__main__":
    unittest.main()
