"""
Send sequences to all open terminals.
"""
import os
import pathlib
import re

from pywal import settings as s
from pywal import util


def set_special(index, color):
    """Build the escape sequence for special colors."""
    s.ColorType.sequences.append(f"\\033]{index};{color}\\007")

    if index == 10:
        s.ColorType.xrdb.append(f"URxvt*foreground: {color}")
        s.ColorType.xrdb.append(f"XTerm*foreground: {color}")

    elif index == 11:
        s.ColorType.xrdb.append(f"URxvt*background: {color}")
        s.ColorType.xrdb.append(f"XTerm*background: {color}")

    elif index == 12:
        s.ColorType.xrdb.append(f"URxvt*cursorColor: {color}")
        s.ColorType.xrdb.append(f"XTerm*cursorColor: {color}")

    elif index == 66:
        s.ColorType.xrdb.append(f"*.color{index}: {color}")
        s.ColorType.xrdb.append(f"*color{index}: {color}")
        s.ColorType.sequences.append(f"\\033]4;{index};{color}\\007")


def set_color(index, color):
    """Build the escape sequence we need for each color."""
    s.ColorType.xrdb.append(f"*.color{index}: {color}")
    s.ColorType.xrdb.append(f"*color{index}: {color}")
    s.ColorType.sequences.append(f"\\033]4;{index};{color}\\007")
    s.ColorType.shell.append(f"color{index}='{color}'")
    s.ColorType.css.append(f"\t--color{index}: {color};")
    s.ColorType.scss.append(f"$color{index}: {color};")

    rgb = util.hex_to_rgb(color)
    s.ColorType.putty.append(f"\"Colour{index}\"=\"{rgb}\"")


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
    set_special(10, colors[15])
    set_special(11, colors[0])
    set_special(12, colors[15])
    set_special(13, colors[15])
    set_special(14, colors[0])

    # This escape sequence doesn"t work in VTE terminals.
    if not vte:
        set_special(708, colors[0])

    # Create the sequences.
    # pylint: disable=W0106
    [set_color(num, color) for num, color in enumerate(colors)]

    # Set a blank color that isn"t affected by bold highlighting.
    set_special(66, colors[0])

    # Make the terminal interpret escape sequences.
    sequences = util.fix_escape("".join(s.ColorType.sequences))

    # Get a list of terminals.
    terminals = [f"/dev/pts/{term}" for term in os.listdir("/dev/pts/")
                 if len(term) < 4]
    terminals.append(s.CACHE_DIR / "sequences")

    # Send the sequences to all open terminals.
    # pylint: disable=W0106
    [util.save_file(sequences, term) for term in terminals]

    print("colors: Set terminal colors")


def reload_colors(vte):
    """Reload colors."""
    sequence_file = pathlib.Path(s.CACHE_DIR / "sequences")

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the problem sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        # Make the terminal interpret escape sequences.
        print(util.fix_escape(sequences), end="")

    exit(0)
