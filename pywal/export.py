"""
Export colors in various formats.
"""
import os
import pathlib

from .settings import CACHE_DIR, MODULE_DIR
from . import util


def template(colors, input_file, output_file=None):
    """Read template file, substitute markers and
       save the file elsewhere."""
    template_data = util.read_file_raw(input_file)
    template_data = "".join(template_data).format(**colors)

    util.save_file(template_data, output_file)


def flatten_colors(colors):
    """Prepare colors to be exported.
       Flatten dicts and convert colors to util.Color()"""
    all_colors = {"wallpaper": colors["wallpaper"],
                  **colors["special"],
                  **colors["colors"]}
    return {k: util.Color(v) for k, v in all_colors.items()}


def get_export_type(export_type):
    """Convert template type to the right filename."""
    return {
        "css": "colors.css",
        "json": "colors.json",
        "konsole": "colors-konsole.colorscheme",
        "putty": "colors-putty.reg",
        "scss": "colors.scss",
        "shell": "colors.sh",
        "xresources": "colors.Xresources",
        "yaml": "colors.yml",
    }.get(export_type, export_type)


def every(colors, output_dir=CACHE_DIR):
    """Export all template files."""
    all_colors = flatten_colors(colors)
    output_dir = pathlib.Path(output_dir)

    for file in os.scandir(MODULE_DIR / "templates"):
        template(all_colors, file.path, output_dir / file.name)

    print("export: Exported all files.")


def color(colors, export_type, output_file=None):
    """Export a single template file."""
    all_colors = flatten_colors(colors)

    template_name = get_export_type(export_type)
    template_file = MODULE_DIR / "templates" / template_name
    output_file = output_file or CACHE_DIR / template_name

    if template_file.is_file():
        template(all_colors, template_file, output_file)
        print(f"export: Exported {export_type}.")
    else:
        print(f"[!] warning: template '{export_type}' doesn't exist.")
