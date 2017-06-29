"""
Export colors in various formats.
"""
import os
import pathlib

from pywal.settings import CACHE_DIR, TEMPLATE_DIR


def template(colors, input_file):
    """Read template file, substitute markers and
        save the file elsewhere."""
    template_file = pathlib.Path(TEMPLATE_DIR).joinpath(input_file)
    export_file = pathlib.Path(CACHE_DIR).joinpath(input_file)

    # Import the template.
    with open(template_file) as file:
        template_data = file.readlines()

    # Merge both dicts.
    colors["colors"].update(colors["special"])

    # Format the markers.
    template_data = "".join(template_data).format(**colors["colors"])

    # Export the template.
    with open(export_file, "w") as file:
        file.write(template_data)


def export_all_templates(colors):
    """Export all template files."""
    # pylint: disable=W0106
    [template(colors, file.name) for file in os.scandir(TEMPLATE_DIR)]
