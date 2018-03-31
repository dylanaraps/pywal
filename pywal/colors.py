"""
Generate a palette using various backends.
"""
import os
import re
import shutil
import sys

from . import backends
from . import util
from .settings import CACHE_DIR, __cache_version__


def list_backends():
    """List color backends."""
    return [backend for backend in dir(backends) if "__" not in backend]


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

        # Dynamic shiz.
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
