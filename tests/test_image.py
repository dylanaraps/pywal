"""Test image functions."""
import unittest

from pywal import image


class TestImage(unittest.TestCase):
    """Test image functions."""
    def test_get_img(self):
        """> Validate image file."""
        result = image.get("tests/test_files/test.jpg")
        self.assertIn("tests/test_files/test.jpg", result)

    def test_get_img_dir(self):
        """> Validate image directory."""
        result = image.get("tests/test_files")
        self.assertEqual(result.endswith((".jpg", ".png")), True)

    def test_get_img_fail(self):
        """> Validate image file. (fail)"""
        with self.assertRaises(SystemExit):
            image.get("tests/test_files/test_fail.jpg")

    def test_get_img_dir_fail(self):
        """> Validate image directory. (fail)"""
        with self.assertRaises(SystemExit):
            image.get("tests")


if __name__ == "__main__":
    unittest.main()
