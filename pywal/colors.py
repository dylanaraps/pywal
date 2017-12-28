"""
Generate a colorscheme using imagemagick.
"""
import os
import numpy
import scipy
import scipy.misc
import scipy.cluster

from PIL import Image
from PIL import ImageEnhance

from .settings import CACHE_DIR, COLOR_COUNT
from . import util


def sort_colors(img, colors):
    """Sort the generated colors and store them in a dict that
       we will later save in json format."""
    # raw_colors = [colors[0], *colors[15:23], *colors[15:23]]
    raw_colors = [colors[0], *colors[8:], *colors[8:]]

    # Darken the background color if it's too light.
    # The value can be a letter or an int so we treat the
    # entire test as strings.
    print(raw_colors[0][1])
    if raw_colors[0][1] not in ["0", "1", "2"]:
        raw_colors[0] = util.darken_color(raw_colors[0], 0.25)

    # Create a comment color from the background.
    raw_colors[8] = util.lighten_color(raw_colors[0], 0.40)

    colors = {}
    colors["wallpaper"] = img
    colors["special"] = {}
    colors["colors"] = {}

    colors["special"]["background"] = raw_colors[0]
    colors["special"]["foreground"] = raw_colors[15]
    colors["special"]["cursor"] = raw_colors[15]

    for index, color in enumerate(raw_colors):
        colors["colors"]["color%s" % index] = color

    return colors


def kmeans(img, color_count):
    """Get colors using kmeans."""
    image = Image.open(img)
    image.thumbnail((100, 100), Image.ANTIALIAS)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.0)

    arr = numpy.asarray(image)
    shape = arr.shape
    arr = arr.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    colors = scipy.cluster.vq.kmeans2(arr, color_count*2)[0]

    if len(colors) < 16:
        print("error: Failed to find enough colors.")
        exit(1)

    colors = [list(map(int, color)) for color in colors.tolist()]

    for color in colors:
        red, gre, blu = color
        color.append((red+red+blu+gre+gre+gre) / 6)

    colors = sorted(colors, key=lambda e: e[3])
    del colors[1::2]

    return ["#%02x%02x%02x" % tuple(color[:-1]) for color in colors]


def get(img, cache_dir=CACHE_DIR,
        color_count=COLOR_COUNT, notify=False):
    """Get the colorscheme."""
    # _home_dylan_img_jpg.json
    cache_file = img.replace("/", "_").replace("\\", "_").replace(".", "_")
    cache_file = os.path.join(cache_dir, "schemes", cache_file + ".json")

    if os.path.isfile(cache_file):
        colors = util.read_file_json(cache_file)
        print("colors: Found cached colorscheme.")

    else:
        util.msg("wal: Generating a colorscheme...", notify)

        colors = kmeans(img, color_count)
        colors = sort_colors(img, colors)

        util.save_file_json(colors, cache_file)
        util.msg("wal: Generation complete.", notify)

    return colors


def file(input_file):
    """Import colorscheme from json file."""
    data = util.read_file_json(input_file)

    if "wallpaper" not in data:
        data["wallpaper"] = "None"

    return data
