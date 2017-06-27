"""Test gen functions."""
import unittest

from pywal import gen_colors


class TestGenColors(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_get_img(self):
        """> Validate image file."""
        result = gen_colors.get_image("tests/test_files/test.jpg")
        self.assertEqual(result, "tests/test_files/test.jpg")

    def test_get_img_dir(self):
        """> Validate image directory."""
        result = gen_colors.get_image("tests/test_files")
        self.assertEqual(result, "tests/test_files/test.jpg")

    def test_gen_colors(self):
        """> Generate a colorscheme."""
        result = gen_colors.gen_colors("tests/test_files/test.jpg")
        self.assertEqual(result[0], "#0F191A")


if __name__ == "__main__":
    unittest.main()
