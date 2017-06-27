"""Test util functions."""
import unittest
import pathlib

from pywal import export_colors
from pywal import util


# Import colors.
COLORS = util.read_file("tests/test_files/test_file")


class TestExportColors(unittest.TestCase):
    """Test the export_colors functions."""

    def test_save_colors(self):
        """> Export colors to a file."""
        tmp_file = pathlib.Path("/tmp/test_file")
        colors = util.read_file("tests/test_files/test_file")
        export_colors.save_colors(colors, tmp_file, "plain colors")
        result = tmp_file.is_file()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
