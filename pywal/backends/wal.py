"""
Generate a colorscheme using imagemagick.
"""
import logging
import re
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def imagemagick(color_count, img, magick_command):
    """Call Imagemagick to generate a scheme."""
    flags = ["-resize", "25%", "-colors", str(color_count),
             "-unique-colors", "txt:-"]
    img += "[0]"

    return subprocess.check_output([*magick_command, img, *flags]).splitlines()


def has_im():
    """Check to see if the user has im installed."""
    if shutil.which("magick"):
        return ["magick", "convert"]

    if shutil.which("convert"):
        return ["convert"]

    logging.error("Imagemagick wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)


def gen_colors(img):
    """Format the output from imagemagick into a list
       of hex colors."""
    magick_command = has_im()

    for i in range(0, 20, 1):
        raw_colors = imagemagick(16 + i, img, magick_command)

        if len(raw_colors) > 16:
            break

        if i == 19:
            logging.error("Imagemagick couldn't generate a suitable palette.")
            sys.exit(1)

        else:
            logging.warning("Imagemagick couldn't generate a palette.")
            logging.warning("Trying a larger palette size %s", 16 + i)

    return [re.search("#.{6}", str(col)).group(0) for col in raw_colors[1:]]


def adjust(cols, light, cols16):
    """Adjust the generated colors and store them in a dict that
       we will later save in json format."""
    raw_colors = cols[:1] + cols[8:16] + cols[8:-1]

    return colors.generic_adjust(raw_colors, light, cols16)


def get(img, light=False, cols16=False):
    """Get colorscheme."""
    colors = gen_colors(img)
    return adjust(colors, light, cols16)
