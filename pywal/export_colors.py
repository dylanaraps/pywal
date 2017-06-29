"""
Export colors in various formats.
"""
import os
import pathlib

from pywal.settings import CACHE_DIR, TEMPLATE_DIR
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


def export_all_templates(colors):
    """Export all template files."""
    # Exclude these templates from the loop.
    # The excluded templates need color
    # conversion or other intervention.
    exclude = ["colors-putty.reg"]

    # Merge both dicts so we can access their
    # values simpler.
    colors["colors"].update(colors["special"])

    # Convert colors to other format.
    colors_rgb = {k: util.hex_to_rgb(v) for k, v in colors["colors"].items()}

    # pylint: disable=W0106
    [template(colors["colors"], file.path, CACHE_DIR)
     for file in os.scandir(TEMPLATE_DIR)
     if file.name not in exclude]

    # Call 'putty' manually since it needs RGB
    # colors.
    putty_file = TEMPLATE_DIR / pathlib.Path("colors-putty.reg")
    template(colors_rgb, putty_file, CACHE_DIR)
