"""Test export functions."""
import unittest
import pathlib

from pywal import export_colors
from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")


class TestExportColors(unittest.TestCase):
    """Test the export_colors functions."""

    def test_template(self):
        """> Test substitutions in template file."""
        # Merge both dicts so we can access their
        # values simpler.
        COLORS["colors"].update(COLORS["special"])

        # Dirs to use.
        tmp_dir = pathlib.Path("/tmp")
        test_template = pathlib.Path("tests/test_files/test_template")
        export_colors.template(COLORS["colors"], test_template, tmp_dir)

        result = pathlib.Path("/tmp/test_template").is_file()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
