"""
Generate a colorscheme using Colorz.
"""
import subprocess

from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    colorz = ["colorz", "-n", "6", "--bold", "0", "--no-preview"]
    return subprocess.check_output([*colorz, img]).splitlines()


def adjust(img, colors, light):
    """Create palette."""
    if light:
        print("colors: Colorz backend doesn't support light themes.")

    raw_colors = ["#000000", *colors, "#FFFFFF",
                  "#333333", *colors, "#FFFFFF"]

    raw_colors[0] = util.darken_color(colors[0], 0.75)
    raw_colors[8] = util.darken_color(colors[0], 0.25)
    raw_colors[7] = util.lighten_color(colors[0], 0.75)
    raw_colors[15] = raw_colors[7]

    colors = {"wallpaper": img,
              "alpha": util.Color.alpha_num,
              "special": {},
              "colors": {}}

    for i, color in enumerate(raw_colors):
        colors["colors"]["color%s" % i] = color

    colors["special"]["background"] = raw_colors[0]
    colors["special"]["foreground"] = raw_colors[15]
    colors["special"]["cursor"] = raw_colors[1]

    return colors


def get(img, light=False):
    """Get colorscheme."""
    colors = gen_colors(img)
    colors = [color.decode('UTF-8').split()[0] for color in colors]
    return adjust(img, colors, light)
