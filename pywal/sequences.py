"""
Send sequences to all open terminals.
"""
import glob
import os

from .settings import CACHE_DIR, OS
from . import util


def set_special(index, color, iterm_name="h"):
    """Convert a hex color to a special sequence."""
    alpha = util.Color.alpha_num

    if OS == "Darwin":
        return "\033]P%s%s\033\\" % (iterm_name, color.strip("#"))

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
    red, green, blue = util.hex_to_rgb(color)
    return """
    \033]6;1;bg;red;brightness;%s\a
    \033]6;1;bg;green;brightness;%s\a
    \033]6;1;bg;blue;brightness;%s\a
    """ % (red, green, blue)


def create_sequences(colors):
    """Create the escape sequences."""
    # Colors 0-15.
    sequences = [set_color(index, colors["colors"]["color%s" % index])
                 for index in range(16)]

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foregound
    # 13 = mouse foreground
    sequences.append(set_special(10, colors["special"]["foreground"], "g"))
    sequences.append(set_special(11, colors["special"]["background"], "h"))
    sequences.append(set_special(12, colors["colors"]["color1"], "l"))

    # Hide the cursor.
    sequences.append(set_special(13, colors["special"]["foreground"], "l"))

    if OS == "Darwin":
        sequences += set_iterm_tab_color(colors["special"]["background"])

    # This escape sequence doesn't work in VTE terminals and their parsing of
    # unknown sequences is garbage so we need to use some escape sequence
    # M A G I C to hide the output.
    # \0337                # Save cursor position.
    # \033[1000H           # Move the cursor off screen.
    # \033[8m              # Conceal text.
    # \033]708;#000000\007 # Garbage sequence.
    # \0338                # Restore cursor position.
    sequences.append("\0337\033[1000H\033[8m\033]708;%s\007\0338" %
                     colors['special']['background'])

    # Show the cursor.
    sequences.append(set_special(13, colors["special"]["cursor"], "l"))

    return "".join(sequences)


def send(colors, cache_dir=CACHE_DIR):
    """Send colors to all open terminals."""
    sequences = create_sequences(colors)

    if OS == "Darwin":
        tty_pattern = "/dev/ttys00[0-9]*"

    else:
        tty_pattern = "/dev/pts/[0-9]*"

    # Writing to "/dev/pts/[0-9] lets you send data to open terminals.
    for term in glob.glob(tty_pattern):
        util.save_file(sequences, term)

    util.save_file(sequences, os.path.join(cache_dir, "sequences"))
    print("colors: Set terminal colors.")
