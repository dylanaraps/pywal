"""
Theme file handling.
"""
import os
import random
import sys

from .settings import CONF_DIR, MODULE_DIR
from . import util


def index():
    """List all installed theme files."""
    themes = [theme for theme in
              os.scandir(os.path.join(CONF_DIR, "colorschemes"))]
    themes += [theme for theme in
               os.scandir(os.path.join(MODULE_DIR, "colorschemes"))]
    return themes


def terminal_sexy_to_wal(data):
    """Convert terminal.sexy json schema to wal."""
    data["colors"] = {}
    data["special"] = {
        "foreground": data["foreground"],
        "background": data["background"],
        "cursor": data["color"][9]
    }

    for i, color in enumerate(data["color"]):
        data["colors"]["color%s" % i] = color

    return data


def file(input_file):
    """Import colorscheme from json file."""
    theme_name = ".".join((input_file, "json"))
    user_theme_file = os.path.join(CONF_DIR, "colorschemes", theme_name)
    theme_file = os.path.join(MODULE_DIR, "colorschemes", theme_name)

    # Find the theme file.
    if os.path.isfile(input_file):
        theme_file = input_file

    elif os.path.isfile(user_theme_file):
        theme_file = user_theme_file

    elif os.path.isfile(theme_file):
        theme_file = theme_file

    elif input_file == "random":
        themes = [theme.path for theme in index()]
        random.shuffle(themes)
        theme_file = themes[0]

    # Parse the theme file.
    if os.path.isfile(theme_file):
        data = util.read_file_json(theme_file)

        if "wallpaper" not in data:
            data["wallpaper"] = "None"

        if "alpha" not in data:
            data["alpha"] = "100"

        # Terminal.sexy format.
        if "color" in data:
            data = terminal_sexy_to_wal(data)

        return data

    else:
        print("No colorscheme file found, exiting...")
        sys.exit(1)
