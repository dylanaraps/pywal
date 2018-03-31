"""
Generate a palette using various backends.
"""
import os
import re
import sys

from . import util
from .settings import CACHE_DIR, MODULE_DIR, __cache_version__


def list_backends():
    """List color backends."""
    return [b.name.replace(".py", "") for b in
            os.scandir(os.path.join(MODULE_DIR, "backends"))
            if "__" not in b.name]


def colors_to_dict(colors, img):
    """Convert list of colors to pywal format."""
    return {
        "wallpaper": img,
        "alpha": util.Color.alpha_num,

        "special": {
            "background": colors[0],
            "foreground": colors[15],
            "cursor": colors[1]
        },

        "colors": {
            "color0": colors[0],
            "color1": colors[1],
            "color2": colors[2],
            "color3": colors[3],
            "color4": colors[4],
            "color5": colors[5],
            "color6": colors[6],
            "color7": colors[7],
            "color8": colors[8],
            "color9": colors[9],
            "color10": colors[10],
            "color11": colors[11],
            "color12": colors[12],
            "color13": colors[13],
            "color14": colors[14],
            "color15": colors[15]
        }
    }


def generic_adjust(colors, light):
    """Generic color adjustment for themers."""
    if light:
        for color in colors:
            color = util.saturate_color(color, 0.50)
            color = util.darken_color(color, 0.4)

        colors[0] = util.lighten_color(colors[0], 0.9)
        colors[7] = util.darken_color(colors[0], 0.75)
        colors[8] = util.darken_color(colors[0], 0.25)
        colors[15] = colors[7]

    else:
        colors[0] = util.darken_color(colors[0], 0.75)
        colors[7] = util.lighten_color(colors[0], 0.75)
        colors[8] = util.lighten_color(colors[0], 0.25)
        colors[15] = colors[7]

    return colors


def cache_fname(img, backend, light, cache_dir):
    """Create the cache file name."""
    color_type = "light" if light else "dark"
    file_name = re.sub("[/|\\|.]", "_", img)

    file_parts = [file_name, color_type, backend, __cache_version__]
    return [cache_dir, "schemes", "%s_%s_%s_%s.json" % (*file_parts,)]


def get(img, light=False, backend="wal", cache_dir=CACHE_DIR):
    """Generate a palette."""
    # home_dylan_img_jpg_backend_1.2.2.json
    cache_name = cache_fname(img, backend, light, cache_dir)
    cache_file = os.path.join(*cache_name)

    if os.path.isfile(cache_file):
        colors = file(cache_file)
        util.Color.alpha_num = colors["alpha"]
        print("colors: Found cached colorscheme.")

    else:
        print("wal: Generating a colorscheme...")

        # Dynamically import the backend we want to use.
        # This keeps the dependencies "optional".
        try:
            __import__("pywal.backends.%s" % backend)
        except ImportError:
            backend = "wal"

        backend = sys.modules["pywal.backends.%s" % backend]
        colors = colors_to_dict(getattr(backend, "get")(img, light), img)

        util.save_file_json(colors, cache_file)
        print("wal: Generation complete.")

    return colors


def file(input_file):
    """Import colorscheme from json file."""
    data = util.read_file_json(input_file)

    if "wallpaper" not in data:
        data["wallpaper"] = "None"

    if "alpha" not in data:
        data["alpha"] = "100"

    return data
