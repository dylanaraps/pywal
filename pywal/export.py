"""
Export colors in various formats.
"""
import os

from pywal.settings import CACHE_DIR
from pywal import util


def template(colors, input_file, output_dir):
    """Read template file, substitute markers and
       save the file elsewhere."""
    # Get the template name.
    template_file = os.path.basename(input_file)

    # Import the template.
    with open(input_file) as file:
        template_data = file.readlines()

    # Format the markers.
    template_data = "".join(template_data).format(**colors)

    # Export the template.
    output_file = output_dir / template_file
    util.save_file(template_data, output_file)

    print(f"export: Exported {template_file}.")


def export_all_templates(colors, template_dir=None, output_dir=CACHE_DIR):
    """Export all template files."""
    # Add the template dir to module path.
    template_dir = template_dir or \
        os.path.join(os.path.dirname(__file__), "templates")

    # Merge all colors (specials and normals) into one dict so we can access
    # their values simpler.
    all_colors = {**colors["special"], **colors["colors"]}

    # Turn all those colors into util.Color instances for accessing the
    # .hex and .rgb formats
    all_colors = {k: util.Color(v) for k, v in all_colors.items()}

    # pylint: disable=W0106
    [template(all_colors, file.path, output_dir)
     for file in os.scandir(template_dir)]
