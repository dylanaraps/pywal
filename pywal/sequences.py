"""
Send sequences to all open terminals.
"""
import glob

from .settings import CACHE_DIR, OS
from . import util


def set_special(index, color, iterm_name="h"):
    """Convert a hex color to a special sequence."""
    alpha = util.Color.alpha_num

    if OS == "Darwin":
        return f"\033]P{iterm_name}{color.strip('#')}\033\\"

    if index in [11, 708] and alpha != 100:
        return f"\033]{index};[{alpha}]{color}\007"

    return f"\033]{index};{color}\007"


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    if OS == "Darwin":
        return f"\033]P{index:x}{color.strip('#')}\033\\"

    return f"\033]4;{index};{color}\007"


def set_iterm_tab_color(color):
    """Set iTerm2 tab/window color"""
    red, green, blue = util.hex_to_rgb(color)
    return [
        f"\033]6;1;bg;red;brightness;{red}\a",
        f"\033]6;1;bg;green;brightness;{green}\a",
        f"\033]6;1;bg;blue;brightness;{blue}\a",
    ]


def create_sequences(colors, vte):
    """Create the escape sequences."""
    # Colors 0-15.
    sequences = [set_color(num, col) for num, col in
                 enumerate(colors["colors"].values())]

    # Set a blank color that isn't affected by bold highlighting.
    # Used in wal.vim's airline theme.
    sequences.append(set_color(66, colors["special"]["background"]))

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foregound
    # 13 = mouse foreground
    sequences.append(set_special(10, colors["special"]["foreground"], "g"))
    sequences.append(set_special(11, colors["special"]["background"], "h"))
    sequences.append(set_special(12, colors["special"]["cursor"], "l"))
    sequences.append(set_special(13, colors["special"]["cursor"], "l"))

    if OS == "Darwin":
        sequences += set_iterm_tab_color(colors["special"]["background"])

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        sequences.append(set_special(708, colors["special"]["background"]))

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

    util.save_file(sequences, cache_dir / "sequences")
    print("colors: Set terminal colors.")
