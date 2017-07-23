"""Test export functions."""
import unittest
import unittest.mock
import io
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

    def test_invalid_template(self):
        """> Test template validation."""
        error_msg = "[!] warning: template 'dummy' doesn't exist."

        # Since this function prints a message on fail we redirect
        # it's output so that we can read it.
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            export.color(COLORS, "dummy", OUTPUT_DIR / "test.css")
            self.assertEqual(fake_out.getvalue().strip(), error_msg)


if __name__ == "__main__":
    unittest.main()
