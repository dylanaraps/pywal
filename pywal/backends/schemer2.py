"""
Generate a colorscheme using Schemer2.
"""
import shutil
import subprocess
import sys

from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    cmd = ["schemer2", "-format", "img::colors", "-minBright", "75", "-in"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(colors, light):
    """Create palette."""
    # Create list with placeholder values.
    colors.sort(key=util.rgb_to_yiq)
    raw_colors = [*colors[8:], *colors[8:]]

    # Update placeholder values.
    if light:
        for color in raw_colors:
            color = util.saturate_color(color, 0.50)
            color = util.darken_color(color, 0.4)

        raw_colors[0] = util.lighten_color(colors[0], 0.9)
        raw_colors[7] = util.darken_color(colors[0], 0.75)
        raw_colors[8] = util.darken_color(colors[0], 0.25)
        raw_colors[15] = raw_colors[7]

    else:
        raw_colors[0] = util.darken_color(colors[0], 0.75)
        raw_colors[7] = util.lighten_color(colors[0], 0.75)
        raw_colors[8] = util.lighten_color(colors[0], 0.25)
        raw_colors[15] = raw_colors[7]

    return raw_colors


def get(img, light=False):
    """Get colorscheme."""
    if not shutil.which("schemer2"):
        print("error: Schemer2 wasn't found on your system.",
              "Try another backend. (wal --backend)")
        sys.exit(1)

    colors = gen_colors(img)
    colors = [color.decode('UTF-8') for color in colors]
    return adjust(colors, light)
