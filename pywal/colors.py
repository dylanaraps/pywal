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
    raw_colors = [colors[0], *colors[8:], *colors[8:]]

    raw_colors[0] = util.darken_color(raw_colors[0], 0.25)
    raw_colors[8] = util.lighten_color(raw_colors[0], 0.40)
    raw_colors[7] = util.lighten_color(raw_colors[7], 0.25)
    raw_colors[15] = util.lighten_color(raw_colors[15], 0.25)

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
    numpy.warnings.filterwarnings('ignore')
    numpy.random.seed(12345)

    # Process the image.
    image = Image.open(img)
    image.thumbnail((100, 100), Image.ANTIALIAS)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)

    # Turn the image into an array.
    arr = numpy.asarray(image)
    arr = arr.reshape(scipy.product(arr.shape[:2]), arr.shape[2]).astype(float)

    centroids, labels = scipy.cluster.vq.kmeans2(arr, color_count,
                                                 check_finite=False,
                                                 minit="points")

    counts = numpy.unique(labels, return_counts=True)[1]
    best_centroid = numpy.argsort(counts)
    colors = centroids[best_centroid].astype(int)
    colors = colors.tolist()

    # Calculate brightness
    for color in colors:
        red, gre, blu = color[:3]
        color.append((red+red+blu+gre+gre+gre) / 6)

    # Sort the colors by brightness.
    colors = sorted(colors, key=lambda e: e[3])

    return ["#%02x%02x%02x" % tuple(color[:3]) for color in colors]


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
