"""Test export functions."""
import unittest
import pathlib

from pywal import export_colors
from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class TestExportColors(unittest.TestCase):
    """Test the export_colors functions."""

    def test_save_colors(self):
        """> Export colors to a file."""
        tmp_file = pathlib.Path("/tmp/test_file.json")
        export_colors.save_colors(COLORS, tmp_file, "plain colors")
        result = tmp_file.is_file()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
