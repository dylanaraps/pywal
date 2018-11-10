"""
Export colors in various formats.
"""
import logging
import os

from .settings import CACHE_DIR, MODULE_DIR, CONF_DIR, HOME
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
    all_colors = {
        "wallpaper": colors["wallpaper"],
        "alpha": colors["alpha"],
        **colors["special"],
        **colors["colors"]
    }
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
        "kitty": "colors-kitty.conf",
        "termite": "colors-termite.conf",
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
    for file in [*os.scandir(template_dir), *os.scandir(template_dir_user)]:
        if file.name != ".DS_Store":
            template(colors, file.path, join(output_dir, file.name))

    # Termite specific as author is too stubborn to include 'include' directive
    # in config file: https://github.com/thestinger/termite/issues/260
    # Only triggered if user has pywal.conf in Termite config as will be
    # explained in the Wiki.
    # The following merges cached Termite colors and the pywal.conf file in
    # ~/.config/termite/ into the standard ~/.config/termite/config

    TERMITE_CONFIG = os.path.join(HOME, '.config/termite/config')
    TERMITE_PYWAL_CONFIG = os.path.join(HOME, '.config/termite/pywal.conf')
    TERMITE_PYWAL_CACHE = os.path.join(CACHE_DIR, 'colors-termite.conf')
    if os.path.isfile(TERMITE_PYWAL_CONFIG):
        configs = [TERMITE_PYWAL_CONFIG, TERMITE_PYWAL_CACHE]
        if not os.path.isfile(TERMITE_CONFIG):
            os.mknod(TERMITE_CONFIG)
        with open(TERMITE_CONFIG, 'w') as outfile:
            for config in configs:
                with open(config) as infile:
                    for line in infile:
                        outfile.write(line)

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
