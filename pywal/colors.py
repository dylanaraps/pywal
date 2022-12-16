"""
Generate a palette using various backends.
"""
import logging
import os
import random
import re
import sys

from . import theme
from . import util
from .settings import CACHE_DIR, MODULE_DIR, __cache_version__


def list_backends():
    """List color backends."""
    return [b.name.replace(".py", "") for b in
            os.scandir(os.path.join(MODULE_DIR, "backends"))
            if "__" not in b.name]

def normalize_img_path(img: str):
    """Normalizes the image path for output."""
    if os.name == 'nt':
        # On Windows, the JSON.dump ends up outputting un-escaped backslash breaking
        # the ability to read colors.json. Windows supports forward slash, so we can
        # use that for now
        return img.replace('\\', '/')
    return img

def colors_to_dict(colors, img):
    """Convert list of colors to pywal format."""
    return {
        "wallpaper": normalize_img_path(img),
        "alpha": util.Color.alpha_num,

        "special": {
            "background": colors[0],
            "foreground": colors[15],
            "cursor": colors[15]
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
            color = util.saturate_color(color, 0.60)
            color = util.darken_color(color, 0.5)

        colors[0] = util.lighten_color(colors[0], 0.95)
        colors[7] = util.darken_color(colors[0], 0.75)
        colors[8] = util.darken_color(colors[0], 0.25)
        colors[15] = colors[7]

    else:
        colors[0] = util.darken_color(colors[0], 0.80)
        colors[7] = util.lighten_color(colors[0], 0.75)
        colors[8] = util.lighten_color(colors[0], 0.25)
        colors[15] = colors[7]

    return colors


def saturate_colors(colors, amount):
    """Saturate all colors."""
    if amount and float(amount) <= 1.0:
        for i, _ in enumerate(colors):
            if i not in [0, 7, 8, 15]:
                colors[i] = util.saturate_color(colors[i], float(amount))

    return colors


def cache_fname(img, backend, light, cache_dir, sat=""):
    """Create the cache file name."""
    color_type = "light" if light else "dark"
    file_name = re.sub("[/|\\|.]", "_", img)
    file_size = os.path.getsize(img)

    file_parts = [file_name, color_type, backend,
                  sat, file_size, __cache_version__]
    return [cache_dir, "schemes", "%s_%s_%s_%s_%s_%s.json" % (*file_parts,)]


def get_backend(backend):
    """Figure out which backend to use."""
    if backend == "random":
        backends = list_backends()
        random.shuffle(backends)
        return backends[0]

    return backend


def palette():
    """Generate a palette from the colors."""
    for i in range(0, 16):
        if i % 8 == 0:
            print()

        if i > 7:
            i = "8;5;%s" % i

        print("\033[4%sm%s\033[0m" % (i, " " * (80 // 20)), end="")

    print("\n")


def get(img, light=False, backend="wal", cache_dir=CACHE_DIR, sat=""):
    """Generate a palette."""
    # home_dylan_img_jpg_backend_1.2.2.json
    cache_name = cache_fname(img, backend, light, cache_dir, sat)
    cache_file = os.path.join(*cache_name)

    if os.path.isfile(cache_file):
        colors = theme.file(cache_file)
        colors["alpha"] = util.Color.alpha_num
        logging.info("Found cached colorscheme.")

    else:
        logging.info("Generating a colorscheme.")
        backend = get_backend(backend)

        # Dynamically import the backend we want to use.
        # This keeps the dependencies "optional".
        try:
            __import__("pywal.backends.%s" % backend)
        except ImportError:
            __import__("pywal.backends.wal")
            backend = "wal"

        logging.info("Using %s backend.", backend)
        backend = sys.modules["pywal.backends.%s" % backend]
        colors = getattr(backend, "get")(img, light)
        colors = colors_to_dict(saturate_colors(colors, sat), img)

        util.save_file_json(colors, cache_file)
        logging.info("Generation complete.")

    return colors


def file(input_file):
    """Deprecated: symbolic link to --> theme.file"""
    return theme.file(input_file)
