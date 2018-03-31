"""
Generate a colorscheme using Colorz.
"""
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    cmd = ["colorz", "-n", "6", "--bold", "0", "--no-preview"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(cols, light):
    """Create palette."""
    bg = util.blend_color("#555555", cols[1])

    raw_colors = [bg, *cols, "#FFFFFF",
                  "#333333", *cols, "#FFFFFF"]

    return colors.generic_adjust(raw_colors, light)


def get(img, light=False):
    """Get colorscheme."""
    if not shutil.which("colorz"):
        print("error: Colorz wasn't found on your system.",
              "Try another backend. (wal --backend)")
        sys.exit(1)

    cols = [col.decode('UTF-8').split()[0] for col in gen_colors(img)]
    return adjust(cols, light)
