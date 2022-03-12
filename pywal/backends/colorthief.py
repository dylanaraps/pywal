"""
Generate a colorscheme using ColorThief.
"""
import logging
import sys

try:
    from colorthief import ColorThief

except ImportError:
    logging.error("ColorThief wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)

from .. import colors
from .. import util


def gen_colors(img):
    """Loop until 16 colors are generated."""
    color_cmd = ColorThief(img).get_palette

    for i in range(0, 10, 1):
        raw_colors = color_cmd(color_count=8 + i)

        if len(raw_colors) >= 8:
            break

        if i == 10:
            logging.error("ColorThief couldn't generate a suitable palette.")
            sys.exit(1)

        else:
            logging.warning("ColorThief couldn't generate a palette.")
            logging.warning("Trying a larger palette size %s", 8 + i)

    return [util.rgb_to_hex(color) for color in raw_colors]


def adjust(cols, light, cols16):
    """Create palette."""
    cols.sort(key=util.rgb_to_yiq)
    raw_colors = [*cols, *cols]

    return colors.generic_adjust(raw_colors, light, cols16)


def get(img, light=False, cols16=False):
    """Get colorscheme."""
    cols = gen_colors(img)
    return adjust(cols, light, cols16)
