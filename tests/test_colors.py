"""Test imagemagick functions."""
import unittest
import unittest.mock
import io

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

    def test_color_cache(self):
        """> Test importing a cached scheme."""
        # Since this function just prints a message we redirect
        # it's output so that we can read it.
        message = "colors: Found cached colorscheme."
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            colors.get("tests/test_files/test.jpg")
            self.assertEqual(fake_out.getvalue().strip(), message)

    def test_color_import(self):
        """> Read colors from a file."""
        result = colors.file("tests/test_files/test_file.json")
        self.assertEqual(result["colors"]["color0"], "#1F211E")


if __name__ == "__main__":
    unittest.main()
