"""
Generate a colorscheme using imagemagick.
"""
import re
import shutil
import subprocess
import sys

from .settings import CACHE_DIR, COLOR_COUNT
from . import util


def imagemagick(color_count, img):
    """Call Imagemagick to generate a scheme."""
    colors = subprocess.Popen(["convert", img, "-resize", "25%",
                               "+dither", "-colors", str(color_count),
                               "-unique-colors", "txt:-"],
                              stdout=subprocess.PIPE)

    return colors.stdout.readlines()


def gen_colors(img, color_count):
    """Format the output from imagemagick into a list
       of hex colors."""
    if not shutil.which("convert"):
        print("error: imagemagick not found, exiting...\n"
              "error: wal requires imagemagick to function.")
        sys.exit(1)

    raw_colors = imagemagick(color_count, img)

    index = 0
    while len(raw_colors) - 1 < color_count:
        index += 1
        raw_colors = imagemagick(color_count + index, img)

        print("colors: Imagemagick couldn't generate a", color_count,
              "color palette, trying a larger palette size",
              color_count + index)

        if index > 20:
            print("colors: Imagemagick couldn't generate a suitable scheme",
                  "for the image. Exiting...")
            sys.exit(1)

    # Remove the first element because it isn't a color code.
    del raw_colors[0]

    return [re.search("#.{6}", str(col)).group(0) for col in raw_colors]


def sort_colors(img, colors):
    """Sort the generated colors and store them in a dict that
       we will later save in json format."""
    raw_colors = colors[:1] + colors[9:] + colors[8:]

    # Darken the background color if it's too light.
    # The value can be a letter or an int so we treat the
    # entire test as strings.
    if raw_colors[0][1] not in ["0", "1", "2"]:
        raw_colors[0] = util.darken_color(raw_colors[0], 0.25)

    # Create a comment color from the background.
    raw_colors[8] = util.lighten_color(raw_colors[0], 0.40)

    colors = {"wallpaper": img}
    colors_special = {}
    colors_hex = {}

    colors_special.update({"background": raw_colors[0]})
    colors_special.update({"foreground": raw_colors[15]})
    colors_special.update({"cursor": raw_colors[15]})

    for index, color in enumerate(raw_colors):
        colors_hex.update({f"color{index}": color})

    colors["special"] = colors_special
    colors["colors"] = colors_hex

    return colors


def get(img, cache_dir=CACHE_DIR,
        color_count=COLOR_COUNT, notify=False):
    """Get the colorscheme."""
    # _home_dylan_img_jpg.json
    cache_file = cache_dir / "schemes" / \
        img.replace("/", "_").replace(".", "_")
    cache_file = cache_file.with_suffix(".json")

    if cache_file.is_file():
        colors = util.read_file_json(cache_file)
        print("colors: Found cached colorscheme.")

    else:
        util.msg("wal: Generating a colorscheme...", notify)

        colors = gen_colors(img, color_count)
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
