"""Test imagemagick functions."""
import unittest

from pywal import wal


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_gen_colors(self):
        """> Generate a colorscheme."""
        result = wal.create_palette("tests/test_files/test.jpg")
        self.assertEqual(result["colors"]["color0"], "#0F191A")


if __name__ == "__main__":
    unittest.main()
