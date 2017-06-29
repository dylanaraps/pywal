"""
Export colors in various formats.
"""
import os
import pathlib

from pywal.settings import CACHE_DIR, TEMPLATE_DIR
from pywal import util


def template(colors, input_file):
    """Read template file, substitute markers and
        save the file elsewhere."""
    template_file = pathlib.Path(TEMPLATE_DIR).joinpath(input_file)
    export_file = pathlib.Path(CACHE_DIR).joinpath(input_file)

    # Import the template.
    with open(template_file) as file:
        template_data = file.readlines()

    # Format the markers.
    template_data = "".join(template_data).format(**colors)

    # Export the template.
    with open(export_file, "w") as file:
        file.write(template_data)

    print(f"export: Exported {input_file}.")


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
    [template(colors["colors"], file.name)
     for file in os.scandir(TEMPLATE_DIR)
     if file not in exclude]

    # Call 'putty' manually since it needs RGB
    # colors.
    template(colors_rgb, "colors-putty.reg")
