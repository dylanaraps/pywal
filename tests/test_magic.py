"""Test imagemagick functions."""
import unittest

from pywal import magic


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_gen_colors(self):
        """> Generate a colorscheme."""
        result = magic.gen_colors("tests/test_files/test.jpg")
        self.assertEqual(result[0], "#0F191A")


if __name__ == "__main__":
    unittest.main()
