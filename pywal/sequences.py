"""
Send sequences to all open terminals.
"""
import glob
import re

from pywal.settings import CACHE_DIR, OS
from pywal import util


def get_color_name(index):
    """Get the color name from a number."""
    return {
        "0":  "black",
        "1":  "red",
        "2":  "green",
        "3":  "yellow",
        "4":  "blue",
        "5":  "magenta",
        "6":  "cyan",
        "7":  "white",
        "8":  "br_black",
        "9":  "br_red",
        "10": "br_green",
        "11": "br_yellow",
        "12": "br_blue",
        "13": "br_magenta",
        "14": "br_cyan",
        "15": "br_white",
    }.get(index, "black")


def get_special_name(index):
    """Get the color name from special number."""
    return {
        "10": "fg",
        "11": "bg",
        "12": "curfg",
        "13": "curfg",
    }.get(index, "black")


def set_special(index, color):
    """Convert a hex color to a special sequence."""
    if OS == "Darwin":
        return f"\033]1337;SetColors={get_color_name(index)}={color}\a"

    return f"\033]{index};{color}\007"


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    if OS == "Darwin":
        return f"\033]1337;SetColors={get_color_name(index)}={color}\a"

    return f"\033]4;{index};{color}\007"


def create_sequences(colors, vte):
    """Create the escape sequences."""
    # Colors 0-15.
    sequences = [set_color(num, color)
                 for num, color in enumerate(colors["colors"].values())]

    # Special colors.
    # http://pod.tst.eu/http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod#XTerm_Operating_System_Commands
    # 10 = foreground, 11 = background, 12 = cursor foregound
    # 13 = mouse foreground
    sequences.append(set_special(10, colors["special"]["foreground"]))
    sequences.append(set_special(11, colors["special"]["background"]))
    sequences.append(set_special(12, colors["special"]["cursor"]))
    sequences.append(set_special(13, colors["special"]["cursor"]))

    # Set a blank color that isn"t affected by bold highlighting.
    # Used in wal.vim's airline theme.
    sequences.append(set_color(66, colors["special"]["background"]))

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        sequences.append(set_special(708, colors["special"]["background"]))

    return sequences


def send_sequences(colors, vte):
    """Send colors to all open terminals."""
    sequences = create_sequences(colors, vte)

    # Get the pseudo terminal directory.
    if OS == "Linux":
        tty_pattern = "/dev/pts/[0-9]*"

    elif OS == "Darwin":
        tty_pattern = "/dev/ttys00[0-9]*"

    # Create a list of pseudo terminals.
    terminals = [term for term in glob.glob(tty_pattern)]

    # Send sequences to cache file as well.
    terminals.append(CACHE_DIR / "sequences")

    # pylint: disable=W0106
    [util.save_file("".join(sequences), term) for term in terminals]
    print("colors: Set terminal colors")


def reload_colors(vte):
    """Reload the current scheme."""
    sequence_file = CACHE_DIR / "sequences"

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the unsupported sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        print(sequences, end="")

    exit(0)
