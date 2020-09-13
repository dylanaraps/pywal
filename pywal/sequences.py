"""
Send sequences to all open terminals.
"""
import glob
import logging
import os

from .settings import CACHE_DIR, OS
from . import util


def set_special(index, color, iterm_name="h", alpha=100):
    """Convert a hex color to a special sequence."""
    if OS == "Darwin" and iterm_name:
        return "\033]P%s%s\033\\" % (iterm_name, color.strip("#"))

    if index in [11, 708] and alpha != "100":
        return "\033]%s;[%s]%s\033\\" % (index, alpha, color)

    return "\033]%s;%s\033\\" % (index, color)


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    if OS == "Darwin" and index < 20:
        return "\033]P%1x%s\033\\" % (index, color.strip("#"))

    return "\033]4;%s;%s\033\\" % (index, color)


def set_iterm_tab_color(color):
    """Set iTerm2 tab/window color"""
    return ("\033]6;1;bg;red;brightness;%s\a"
            "\033]6;1;bg;green;brightness;%s\a"
            "\033]6;1;bg;blue;brightness;%s\a") % (*util.hex_to_rgb(color),)


def create_sequences(colors, vte_fix=False):
    """Create the escape sequences."""
    alpha = colors["alpha"]

    # Colors 0-15.
    sequences = [set_color(index, colors["colors"]["color%s" % index])
                 for index in range(16)]

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foreground
    # 13 = mouse foreground, 708 = background border color.
    sequences.extend([
        set_special(10, colors["special"]["foreground"], "g"),
        set_special(11, colors["special"]["background"], "h", alpha),
        set_special(12, colors["special"]["cursor"], "l"),
        set_special(13, colors["special"]["foreground"], "j"),
        set_special(17, colors["special"]["foreground"], "k"),
        set_special(19, colors["special"]["background"], "m"),
        set_color(232, colors["special"]["background"]),
        set_color(256, colors["special"]["foreground"]),
        set_color(257, colors["special"]["background"]),
    ])

    if not vte_fix:
        sequences.extend(
            set_special(708, colors["special"]["background"], "", alpha)
        )

    if OS == "Darwin":
        sequences += set_iterm_tab_color(colors["special"]["background"])

    return "".join(sequences)


def send(colors, cache_dir=CACHE_DIR, to_send=True, vte_fix=False):
    """Send colors to all open terminals."""
    if OS == "Darwin":
        tty_pattern = "/dev/ttys00[0-9]*"

    else:
        tty_pattern = "/dev/pts/[0-9]*"

    sequences = create_sequences(colors, vte_fix)

    # Writing to "/dev/pts/[0-9] lets you send data to open terminals.
    if to_send:
        for term in glob.glob(tty_pattern):
            util.save_file(sequences, term)

    util.save_file(sequences, os.path.join(cache_dir, "sequences"))
    logging.info("Set terminal colors.")
