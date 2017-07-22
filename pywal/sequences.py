"""
Send sequences to all open terminals.
"""
import os
import re

from pywal import util


def set_special(index, color):
    """Convert a hex color to a special sequence."""
    return f"\033]{index};{color}\007"


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    return f"\033]4;{index};{color}\007"


def send_sequences(colors, vte, cache_dir):
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


def reload_colors(vte, cache_dir):
    """Reload the current scheme."""
    sequence_file = cache_dir / "sequences"

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the unsupported sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        print(sequences, end="")

    exit(0)
