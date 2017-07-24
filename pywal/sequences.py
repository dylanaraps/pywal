"""
Send sequences to all open terminals.
"""
import os

from .settings import CACHE_DIR
from . import util


def set_special(index, color):
    """Convert a hex color to a special sequence."""
    alpha = util.Color.alpha_num

    if index in [11, 708] and alpha != 100:
        return f"\033]{index};[{alpha}]{color}\007"

    return f"\033]{index};{color}\007"


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    return f"\033]4;{index};{color}\007"


def send(colors, vte, cache_dir=CACHE_DIR):
    """Send colors to all open terminals."""
    # Colors 0-15.
    sequences = [set_color(num, color)
                 for num, color in enumerate(colors["colors"].values())]

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foregound
    # 13 = mouse foreground
    sequences.append(set_special(10, colors["special"]["foreground"]))
    sequences.append(set_special(11, colors["special"]["background"]))
    sequences.append(set_special(12, colors["special"]["cursor"]))
    sequences.append(set_special(13, colors["special"]["cursor"]))

    # Set a blank color that isn't affected by bold highlighting.
    # Used in wal.vim's airline theme.
    sequences.append(set_color(66, colors["special"]["background"]))

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        sequences.append(set_special(708, colors["special"]["background"]))

    terminals = [f"/dev/pts/{term}" for term in os.listdir("/dev/pts/")
                 if len(term) < 4]
    terminals.append(cache_dir / "sequences")

    # Writing to "/dev/pts/[0-9] lets you send data to open terminals.
    for term in terminals:
        util.save_file("".join(sequences), term)

    print("colors: Set terminal colors")
