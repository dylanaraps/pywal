"""Test image functions."""
import unittest

from pywal import image


class TestImage(unittest.TestCase):
    """Test image functions."""
    def test_get_img(self):
        """> Validate image file."""
        result = image.get_image("tests/test_files/test.jpg")
        self.assertEqual(result, "tests/test_files/test.jpg")

    def test_get_img_dir(self):
        """> Validate image directory."""
        result = image.get_image("tests/test_files")
        self.assertEqual(result, "tests/test_files/test.jpg")


if __name__ == "__main__":
    unittest.main()
