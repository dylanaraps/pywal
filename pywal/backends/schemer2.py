"""
Generate a colorscheme using Schemer2.
"""
import logging
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    cmd = ["schemer2", "-format", "img::colors", "-minBright", "75", "-in"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(cols, light):
    """Create palette."""
    cols.sort(key=util.rgb_to_yiq)
    raw_colors = [*cols[8:], *cols[8:]]

    return colors.generic_adjust(raw_colors, light)


def get(img, light=False):
    """Get colorscheme."""
    if not shutil.which("schemer2"):
        logging.error("Schemer2 wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = [col.decode('UTF-8') for col in gen_colors(img)]
    return adjust(cols, light)
