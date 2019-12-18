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
    for i in range(len(template_data)):
        line = template_data[i]
        matches = re.finditer(r"(?<=(?<!\{))(\{([^{}]+)\})(?=(?!\}))", line)
        for match in matches:
            # Check that this color doesn't already exist
            color, _, funcs = match.group(2).partition(".")
            if len(funcs) != 0:
                to_replace = color
                new_color = None
                for func in funcs.split(")"):
                    if len(func) == 0:
                        continue
                    func_split = func.split("(")
                    if len(func_split) > 1:
                        args = func_split[1].split(",")
                    else:
                        args = []
                    name = func_split[0]
                    if name[0] == '.':
                        name = name[1:]
                    x = getattr(colors[color], name)
                    if callable(x):
                        new_color = x(*args)
                        if func[0] != '.':
                            to_replace += "."
                        to_replace += func + ")"
                    else:
                        pass
                if not new_color is None:
                    cname = "color" + new_color.strip
                    template_data[i] = line.replace(to_replace, cname)
                    colors[cname] = new_color
    try:
        template_data = "".join(template_data).format(**colors)
    except ValueError:
        logging.error("Syntax error in template file '%s'.", input_file)
        return
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
        "dmenu": "colors-wal-dmenu.h",
        "dwm": "colors-wal-dwm.h",
        "st": "colors-wal-st.h",
        "tabbed": "colors-wal-tabbed.h",
        "gtk2": "colors-gtk2.rc",
        "json": "colors.json",
        "konsole": "colors-konsole.colorscheme",
        "kitty": "colors-kitty.conf",
        "plain": "colors",
        "putty": "colors-putty.reg",
        "rofi": "colors-rofi.Xresources",
        "scss": "colors.scss",
        "shell": "colors.sh",
        "speedcrunch": "colors-speedcrunch.json",
        "sway": "colors-sway",
        "tty": "colors-tty.sh",
        "waybar": "colors-waybar.css",
        "xresources": "colors.Xresources",
        "xmonad": "colors.hs",
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
        if file.name != ".DS_Store" and not file.name.endswith(".swp"):
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
