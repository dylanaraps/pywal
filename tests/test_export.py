"""Test export functions."""
import unittest
import pathlib

from pywal import export
from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")
COLORS["colors"].update(COLORS["special"])
OUTPUT_DIR = pathlib.Path("/tmp/wal")

util.create_dir("/tmp/wal")


class TestExportColors(unittest.TestCase):
    """Test the export functions."""

    def test_all_templates(self):
        """> Test substitutions in template file."""
        export.every(COLORS, OUTPUT_DIR)

        result = pathlib.Path("/tmp/wal/colors.sh").is_file()
        self.assertTrue(result)

        content = pathlib.Path("/tmp/wal/colors.sh").read_text()
        content = content.split("\n")[6]
        self.assertEqual(content, "foreground='#F5F1F4'")

    def test_css_template(self):
        """> Test substitutions in template file (css)."""
        export.color(COLORS, "css", OUTPUT_DIR / "test.css")

        result = pathlib.Path("/tmp/wal/test.css").is_file()
        self.assertTrue(result)

        content = pathlib.Path("/tmp/wal/test.css").read_text()
        content = content.split("\n")[6]
        self.assertEqual(content, "    --background: #1F211E;")


if __name__ == "__main__":
    unittest.main()
