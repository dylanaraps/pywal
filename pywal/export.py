"""
Export colors in various formats.
"""
import logging
import os
import re

from .settings import CACHE_DIR, MODULE_DIR, CONF_DIR
from . import util


def template(colors, input_file, output_file=None):
    """Read template file, substitute markers and
       save the file elsewhere."""
    template_data = util.read_file_raw(input_file)

    # Match all substitution markers
    matches = re.finditer(r"(?<!{){[^{|}]+}", "".join(template_data),
                          re.MULTILINE)

    for match in matches:
        # Check that this color doesn't already exist
        match_str = match.group().strip("{}")
        if match_str not in colors:
            # Extract original color and functions
            attr, _, pieces = match_str.partition(".")
            attr = colors[attr]
            pieces = pieces.split(".")
            # Apply every function to the original color
            for piece in pieces:
                # Check if this sub-color has already been generated
                if not hasattr(attr, piece):
                    # Generate new color using function from util.py
                    func, arg = piece.strip(")").split("(")
                    arg = arg.split(",")
                    new_color = util.Color(
                        getattr(util, func)(attr.hex_color, *arg))
                    setattr(attr, piece, new_color)
                    attr = getattr(attr, piece)

    template_data = "".join(template_data).format(**colors)
    util.save_file(template_data, output_file)


def flatten_colors(colors):
    """Prepare colors to be exported.
       Flatten dicts and convert colors to util.Color()"""
    all_colors = {"wallpaper": colors["wallpaper"],
                  "alpha": colors["alpha"],
                  **colors["special"],
                  **colors["colors"]}
    return {k: util.Color(v) for k, v in all_colors.items()}


def get_export_type(export_type):
    """Convert template type to the right filename."""
    return {
        "css": "colors.css",
        "dwm": "colors-wal-dwm.h",
        "st": "colors-wal-st.h",
        "tabbed": "colors-wal-tabbed.h",
        "gtk2": "colors-gtk2.rc",
        "json": "colors.json",
        "konsole": "colors-konsole.colorscheme",
        "plain": "colors",
        "putty": "colors-putty.reg",
        "rofi": "colors-rofi.Xresources",
        "scss": "colors.scss",
        "shell": "colors.sh",
        "sway": "colors-sway",
        "tty": "colors-tty.sh",
        "xresources": "colors.Xresources",
        "yaml": "colors.yml",
    }.get(export_type, export_type)


def every(colors, output_dir=CACHE_DIR):
    """Export all template files."""
    colors = flatten_colors(colors)
    template_dir = os.path.join(MODULE_DIR, "templates")
    template_dir_user = os.path.join(CONF_DIR, "templates")
    util.create_dir(template_dir_user)

    join = os.path.join  # Minor optimization.
    for file in [*os.scandir(template_dir),
                 *os.scandir(template_dir_user)]:
        if file.name != ".DS_Store":
            template(colors, file.path, join(output_dir, file.name))

    logging.info("Exported all files.")
    logging.info("Exported all user files.")


def color(colors, export_type, output_file=None):
    """Export a single template file."""
    all_colors = flatten_colors(colors)

    template_name = get_export_type(export_type)
    template_file = os.path.join(MODULE_DIR, "templates", template_name)
    output_file = output_file or os.path.join(CACHE_DIR, template_name)

    if os.path.isfile(template_file):
        template(all_colors, template_file, output_file)
        logging.info("Exported %s.", export_type)
    else:
        logging.warning("Template '%s' doesn't exist.", export_type)
