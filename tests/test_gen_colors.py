"""Test gen functions."""
import unittest

from pywal import gen_colors
from pywal import util


# Import colors.
COLORS = util.read_file("tests/test_file")


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_get_img(self):
        """> Validate image file."""
        result = gen_colors.get_image("tests/test.jpg")
        self.assertEqual(result, "tests/test.jpg")

    def test_get_img_dir(self):
        """> Validate image directory."""
        result = gen_colors.get_image("tests")
        self.assertEqual(result, "tests/test.jpg")


if __name__ == "__main__":
    unittest.main()
