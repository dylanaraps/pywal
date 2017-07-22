"""
Export colors in various formats.
"""
import os
import pathlib

from .settings import __cache_dir__
from . import util


TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"


def template(colors, input_file, cache_dir):
    """Read template file, substitute markers and
       save the file elsewhere."""
    template_data = util.read_file_raw(input_file)
    template_data = "".join(template_data).format(**colors)
    template_name = os.path.basename(input_file)

    util.save_file(template_data, cache_dir / template_name)
    print(f"export: Exported {template_name}.")


def flatten_colors(colors):
    """Prepare colors to be exported. (Flatten dicts)"""
    all_colors = {"wallpaper": colors["wallpaper"],
                  **colors["special"],
                  **colors["colors"]}
    return {k: util.Color(v) for k, v in all_colors.items()}


def export_all(colors, cache_dir=__cache_dir__):
    """Export all template files."""
    all_colors = flatten_colors(colors)

    for file in os.scandir(TEMPLATE_DIR):
        template(all_colors, file.path, cache_dir)


def export(colors, file, cache_dir=__cache_dir__):
    """Export a single template file."""
    all_colors = flatten_colors(colors)
    template_file = TEMPLATE_DIR / file

    if template_file.is_file():
        template(all_colors, template_file, cache_dir)
    else:
        print(f"[!] warning: template '{template_file}' doesn't exist.")
