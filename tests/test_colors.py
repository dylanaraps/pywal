"""Test imagemagick functions."""
import unittest

from pywal import colors


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_gen_colors(self):
        """> Generate a colorscheme."""
        result = colors.get("tests/test_files/test.jpg")
        self.assertEqual(len(result["colors"]["color0"]), 7)

    def test_gen_colors_fail(self):
        """> Generate a colorscheme and fail."""
        with self.assertRaises(SystemExit):
            colors.get("tests/test_files/test.png")


if __name__ == "__main__":
    unittest.main()
