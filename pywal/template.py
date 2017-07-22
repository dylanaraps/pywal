"""
Export colors in various formats.
"""
import os

from pywal import util


def template(colors, input_file, output_dir):
    """Read template file, substitute markers and
       save the file elsewhere."""
    template_data = util.read_file_raw(input_file)
    template_data = "".join(template_data).format(**colors)
    template_name = os.path.basename(input_file)
    util.save_file(template_data, output_dir / template_name)
    print(f"export: Exported {template_name}.")


def export_all_templates(colors, output_dir, template_dir=None):
    """Export all template files."""
    template_dir = template_dir or \
        os.path.join(os.path.dirname(__file__), "templates")

    all_colors = {"wallpaper": colors["wallpaper"],
                  **colors["special"],
                  **colors["colors"]}
    all_colors = {k: util.Color(v) for k, v in all_colors.items()}

    # pylint: disable=W0106
    [template(all_colors, file.path, output_dir)
     for file in os.scandir(template_dir)]
