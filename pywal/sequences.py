"""
Send sequences to all open terminals.
"""
import glob
import os

from .settings import CACHE_DIR, OS
from . import util


def set_special(index, color, iterm_name="bg"):
    """Convert a hex color to a special sequence."""
    alpha = util.Color.alpha_num

    if OS == "Darwin":
        return "\033]1337;SetColors=%s=%s\a" % (iterm_name, color.strip("#"))

    if index in [11, 708] and alpha != 100:
        return "\033]%s;[%s]%s\007" % (index, alpha, color)

    return "\033]%s;%s\007" % (index, color)


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    if OS == "Darwin":
        return "\033]P%x%s\033\\" % (index, color.strip("#"))

    return "\033]4;%s;%s\007" % (index, color)


def set_iterm_tab_color(color):
    """Set iTerm2 tab/window color"""
    return "\033]1337;SetColors=tab=%s\a" % color.strip("#")


def create_sequences(colors, vte):
    """Create the escape sequences."""
    # Colors 0-15.
    sequences = [set_color(index, colors["colors"]["color%s" % index])
                 for index in range(16)]

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        sequences.append(set_special(708, colors["special"]["background"]))

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foregound
    # 13 = mouse foreground
    sequences.append(set_special(10, colors["special"]["foreground"], "fg"))
    sequences.append(set_special(11, colors["special"]["background"], "bg"))
    sequences.append(set_special(12, colors["special"]["cursor"], "curbg"))
    sequences.append(set_special(13, colors["special"]["cursor"], "curbg"))

    if OS == "Darwin":
        sequences += set_iterm_tab_color(colors["special"]["background"])

    return "".join(sequences)


def send(colors, vte, cache_dir=CACHE_DIR):
    """Send colors to all open terminals."""
    sequences = create_sequences(colors, vte)

    if OS == "Darwin":
        tty_pattern = "/dev/ttys00[0-9]*"

    else:
        tty_pattern = "/dev/pts/[0-9]*"

    # Writing to "/dev/pts/[0-9] lets you send data to open terminals.
    for term in glob.glob(tty_pattern):
        util.save_file(sequences, term)

    util.save_file(sequences, os.path.join(cache_dir, "sequences"))
    print("colors: Set terminal colors.")
