"""
Generate a palette using various backends.
"""
import re
import os

from . import backends
from . import util
from .settings import CACHE_DIR, __cache_version__


def get(backend_type="wal"):
    """Get backend function name from name."""
    return {
        "colorthief": backends.colorthief.get,
        "colorz": backends.colorz.get,
        "wal": backends.wal.get,
    }.get(backend_type, backends.wal.get)


def list_backends():
    """List color backends."""
    # TODO: Dynamically generate this.
    return "colorthief, colorz, wal"


def colors_to_dict(colors, img):
    """Convert list of colors to pywal format."""
    scheme = {"wallpaper": img,
              "alpha": util.Color.alpha_num,
              "special": {},
              "colors": {}}

    for i, color in enumerate(colors):
        scheme["colors"]["color%s" % i] = color

    scheme["special"]["background"] = colors[0]
    scheme["special"]["foreground"] = colors[15]
    scheme["special"]["cursor"] = colors[1]

    return scheme


def gen(img, light=False, backend="wal", cache_dir=CACHE_DIR):
    """Generate a palette."""
    # home_dylan_img_jpg_backend_1.2.2.json
    color_type = "light" if light else "dark"
    cache_file = re.sub("[/|\\|.]", "_", img)
    cache_file = os.path.join(cache_dir, "schemes", "%s_%s_%s_%s.json"
                              % (cache_file, color_type,
                                 backend, __cache_version__))

    if os.path.isfile(cache_file):
        colors = file(cache_file)
        util.Color.alpha_num = colors["alpha"]
        print("colors: Found cached colorscheme.")

    else:
        print("wal: Generating a colorscheme...")

        colors = get(backend)(img, light)
        colors = colors_to_dict(colors, img)

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
