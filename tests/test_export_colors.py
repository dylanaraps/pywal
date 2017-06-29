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

        output_dir = pathlib.Path("/tmp")
        template_dir = pathlib.Path("tests/test_files/templates")
        export_colors.export_all_templates(COLORS, template_dir, output_dir)

        result = pathlib.Path("/tmp/test_template").is_file()
        self.assertTrue(result)

        content = pathlib.Path("/tmp/test_template").read_text()
        self.assertEqual(content, '\n'.join(["test1 #3A5130",
                                             "test2 #3A5130",
                                             "test3 58,81,48", ""]))


if __name__ == "__main__":
    unittest.main()
