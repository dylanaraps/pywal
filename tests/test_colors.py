"""Test imagemagick functions."""
import unittest

from pywal import colors


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_gen_colors(self):
        """> Generate a colorscheme."""
        result = colors.get("tests/test_files/test.jpg")
        self.assertEqual(result["colors"]["color0"], "#0D191B")


if __name__ == "__main__":
    unittest.main()
