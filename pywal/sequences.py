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
    if OS == "Darwin":
        return "\033]P%s%s\033\\" % (iterm_name, color.strip("#"))

    if index in [11, 708] and alpha != "100":
        return "\033]%s;[%s]%s\033\\" % (index, alpha, color)

    return "\033]%s;%s\033\\" % (index, color)


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    if OS == "Darwin":
        return "\033]P%x%s\033\\" % (index, color.strip("#"))

    return "\033]4;%s;%s\033\\" % (index, color)


def set_iterm_tab_color(color):
    """Set iTerm2 tab/window color"""
    return """
    \033]6;1;bg;red;brightness;%s\a
    \033]6;1;bg;green;brightness;%s\a
    \033]6;1;bg;blue;brightness;%s\a
    """ % (*util.hex_to_rgb(color),)


def create_sequences(colors):
    """Create the escape sequences."""
    alpha = colors["alpha"]

    # Colors 0-15.
    sequences = [set_color(index, colors["colors"]["color%s" % index])
                 for index in range(16)]

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foregound
    # 13 = mouse foreground
    sequences.extend([
        set_special(10, colors["special"]["foreground"], "g"),
        set_special(11, colors["special"]["background"], "h", alpha),
        set_special(12, colors["special"]["cursor"], "l"),
        set_special(13, colors["special"]["foreground"], "l"),
        set_special(17, colors["special"]["foreground"], "l"),
        set_special(19, colors["special"]["background"], "l"),
        set_color(232, colors["special"]["background"])
    ])

    # This escape sequence doesn't work in VTE terminals and their parsing of
    # unknown sequences is garbage so we need to use some escape sequence
    # M A G I C to hide the output.
    # \033[s                 # Save cursor position.
    # \033[1000H             # Move the cursor off screen.
    # \033[8m                # Conceal text.
    # \033]708;#000000\033\\ # Garbage sequence.
    # \033[u                 # Restore cursor position.
    sequences.extend([
        "\033[s\033[1000H\033[8m%s\033[u" %
        set_special(708, colors["special"]["background"], "h", alpha),
        set_special(13, colors["special"]["cursor"], "l")
    ])

    if OS == "Darwin":
        sequences += set_iterm_tab_color(colors["special"]["background"])

    return "".join(sequences)


def send(colors, cache_dir=CACHE_DIR, to_send=True):
    """Send colors to all open terminals."""
    if OS == "Darwin":
        tty_pattern = "/dev/ttys00[0-9]*"

    else:
        tty_pattern = "/dev/pts/[0-9]*"

    sequences = create_sequences(colors)

    # Writing to "/dev/pts/[0-9] lets you send data to open terminals.
    if to_send:
        for term in glob.glob(tty_pattern):
            util.save_file(sequences, term)

    util.save_file(sequences, os.path.join(cache_dir, "sequences"))
    logging.info("Set terminal colors.")
