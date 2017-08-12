"""Test export functions."""
import unittest
import unittest.mock
import io
import os

from pywal import export
from pywal import util


# Import colors.
COLORS = util.read_file_json("tests/test_files/test_file.json")
COLORS["colors"].update(COLORS["special"])

util.create_dir("/tmp/wal")


class TestExportColors(unittest.TestCase):
    """Test the export functions."""

    def test_all_templates(self):
        """> Test substitutions in template file."""
        export.every(COLORS, "/tmp/wal")

        result = os.path.isfile("/tmp/wal/colors.sh")
        self.assertTrue(result)

        with open("/tmp/wal/colors.sh") as file:
            content = file.read().splitlines()

        self.assertEqual(content[6], "foreground='#F5F1F4'")

    def test_css_template(self):
        """> Test substitutions in template file (css)."""
        export.color(COLORS, "css", "/tmp/wal/test.css")

        result = os.path.isfile("/tmp/wal/test.css")
        self.assertTrue(result)

        with open("/tmp/wal/test.css") as file:
            content = file.read().splitlines()

        self.assertEqual(content[6], "    --background: #1F211E;")

    def test_invalid_template(self):
        """> Test template validation."""
        error_msg = "warning: template 'dummy' doesn't exist."

        # Since this function prints a message on fail we redirect
        # it's output so that we can read it.
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            export.color(COLORS, "dummy", "/tmp/wal/test.css")
            self.assertEqual(fake_out.getvalue().strip(), error_msg)


if __name__ == "__main__":
    unittest.main()
