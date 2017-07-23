"""Test imagemagick functions."""
import unittest

from pywal import colors


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_gen_colors(self):
        """> Generate a colorscheme."""
        result = colors.get("tests/test_files/test.jpg")
        self.assertEqual(len(result["colors"]["color0"]), 7)


if __name__ == "__main__":
    unittest.main()
