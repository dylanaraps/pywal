"""
Generate a colorscheme using imagemagick.
"""
import os
import re
import shutil
import subprocess
import sys

from .settings import CACHE_DIR, COLOR_COUNT, __cache_version__
from . import util


def imagemagick(color_count, img, magick_command):
    """Call Imagemagick to generate a scheme."""
    flags = ["-resize", "25%", "-colors", str(color_count),
             "-unique-colors", "txt:-"]

    return subprocess.check_output([*magick_command, img, *flags]).splitlines()


def has_im():
    """Check to see if the user has im installed."""
    if shutil.which("magick"):
        return ["magick", "convert"]

    elif shutil.which("convert"):
        return ["convert"]

    print("error: imagemagick not found, exiting...\n"
          "error: wal requires imagemagick to function.")
    sys.exit(1)


def gen_colors(img, color_count):
    """Format the output from imagemagick into a list
       of hex colors."""
    magick_command = has_im()

    for i in range(0, 20, 1):
        raw_colors = imagemagick(color_count + i, img, magick_command)

        if len(raw_colors) > 16:
            break

        elif i == 19:
            print("colors: Imagemagick couldn't generate a suitable scheme",
                  "for the image. Exiting...")
            sys.exit(1)

        else:
            print("colors: Imagemagick couldn't generate a %s color palette, "
                  "trying a larger palette size %s."
                  % (color_count, color_count + i))

    return [re.search("#.{6}", str(col)).group(0) for col in raw_colors[1:]]


def create_palette(img, colors, light):
    """Sort the generated colors and store them in a dict that
       we will later save in json format."""
    raw_colors = colors[:1] + colors[8:16] + colors[8:-1]

    if light:
        # Manually adjust colors.
        raw_colors[7] = raw_colors[0]
        raw_colors[0] = util.lighten_color(raw_colors[15], 0.85)
        raw_colors[15] = raw_colors[7]
        raw_colors[8] = util.lighten_color(raw_colors[7], 0.25)

    else:
        # Darken the background color slightly.
        if raw_colors[0][1] != "0":
            raw_colors[0] = util.darken_color(raw_colors[0], 0.25)

        # Manually adjust colors.
        raw_colors[7] = util.blend_color(raw_colors[7], "#EEEEEE")
        raw_colors[8] = util.darken_color(raw_colors[7], 0.30)
        raw_colors[15] = util.blend_color(raw_colors[15], "#EEEEEE")

    colors = {"wallpaper": img, "alpha": util.Color.alpha_num,
              "special": {}, "colors": {}}
    colors["special"]["background"] = raw_colors[0]
    colors["special"]["foreground"] = raw_colors[15]
    colors["special"]["cursor"] = raw_colors[15]

    if light:
        for i, color in enumerate(raw_colors):
            colors["colors"]["color%s" % i] = util.saturate_color(color, 0.5)

        colors["colors"]["color0"] = raw_colors[0]
        colors["colors"]["color7"] = raw_colors[15]
        colors["colors"]["color8"] = util.darken_color(raw_colors[0], 0.5)
        colors["colors"]["color15"] = raw_colors[15]

    else:
        for i, color in enumerate(raw_colors):
            colors["colors"]["color%s" % i] = color

    return colors


def get(img, cache_dir=CACHE_DIR,
        color_count=COLOR_COUNT, light=False):
    """Get the colorscheme."""
    # home_dylan_img_jpg_1.2.2.json
    color_type = "light" if light else "dark"
    cache_file = re.sub("[/|\\|.]", "_", img)
    cache_file = os.path.join(cache_dir, "schemes", "%s_%s_%s.json"
                              % (cache_file, color_type, __cache_version__))

    if os.path.isfile(cache_file):
        colors = file(cache_file)
        util.Color.alpha_num = colors["alpha"]
        print("colors: Found cached colorscheme.")

    else:
        print("wal: Generating a colorscheme...")

        colors = gen_colors(img, color_count)
        colors = create_palette(img, colors, light)

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
