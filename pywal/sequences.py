"""
Send sequences to all open terminals.
"""
import os
import re

from pywal.settings import CACHE_DIR
from pywal import util


def set_special(index, color):
    """Build the escape sequence for special colors."""
    return f"\033]{index};{color}\007"


def set_color(index, color):
    """Build the escape sequence we need for each color."""
    return f"\033]4;{index};{color}\007"


def send_sequences(colors, vte):
    """Send colors to all open terminals."""
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
    sequences.append(set_color(66, colors["special"]["background"]))

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        sequences.append(set_special(708, colors["special"]["background"]))

    # Get a list of terminals.
    terminals = [f"/dev/pts/{term}" for term in os.listdir("/dev/pts/")
                 if len(term) < 4]
    terminals.append(CACHE_DIR / "sequences")

    # Send the sequences to all open terminals.
    # pylint: disable=W0106
    [util.save_file("".join(sequences), term) for term in terminals]

    print("colors: Set terminal colors")


def reload_colors(vte):
    """Reload colors."""
    sequence_file = CACHE_DIR / "sequences"

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the problem sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        # Make the terminal interpret escape sequences.
        print(sequences, end="")

    exit(0)
