"""
Send sequences to all open terminals.
"""
import os
import pathlib
import re

from pywal.settings import CACHE_DIR
from pywal import util


def set_special(index, color):
    """Build the escape sequence for special colors."""
    return f"\033]{index};{color}\007"


def set_color(index, color):
    """Build the escape sequence we need for each color."""
    return f"\033]4;{index};{color}\007"


def set_grey(colors):
    """Set a grey color based on brightness of color0."""
    return {
        0: "#666666",
        1: "#666666",
        2: "#757575",
        3: "#999999",
        4: "#999999",
        5: "#8a8a8a",
        6: "#a1a1a1",
        7: "#a1a1a1",
        8: "#a1a1a1",
        9: "#a1a1a1",
    }.get(int(colors[0][1]), colors[7])


def send_sequences(colors, vte):
    """Send colors to all open terminals."""
    sequences = [set_color(num, color) for num, color in enumerate(colors)]
    sequences.append(set_special(10, colors[15]))
    sequences.append(set_special(11, colors[0]))
    sequences.append(set_special(12, colors[15]))
    sequences.append(set_special(13, colors[15]))
    sequences.append(set_special(14, colors[0]))

    # Set a blank color that isn"t affected by bold highlighting.
    sequences.append(set_color(66, colors[0]))

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        sequences.append(set_special(708, colors[0]))

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
    sequence_file = pathlib.Path(CACHE_DIR / "sequences")

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the problem sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        # Make the terminal interpret escape sequences.
        print(sequences, end="")

    exit(0)
