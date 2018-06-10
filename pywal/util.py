"""
Misc helper functions.
"""
import colorsys
import json
import logging
import os
import subprocess
import sys


class Color:
    """Color formats."""
    alpha_num = "100"

    def __init__(self, hex_color):
        self.hex_color = hex_color

    def __str__(self):
        return self.hex_color

    @property
    def rgb(self):
        """Convert a hex color to rgb."""
        return "%s,%s,%s" % (*hex_to_rgb(self.hex_color),)

    @property
    def xrgba(self):
        """Convert a hex color to xrdb rgba."""
        return hex_to_xrgba(self.hex_color)

    @property
    def alpha(self):
        """Add URxvt alpha value to color."""
        return "[%s]%s" % (self.alpha_num, self.hex_color)

    @property
    def octal(self):
        """Export color in octal"""
        return "%s%s" % ("#", oct(int(self.hex_color[1:], 16))[2:])

    @property
    def octal_strip(self):
        """Strip '#' from octal color."""
        return oct(int(self.hex_color[1:], 16))[2:]

    @property
    def strip(self):
        """Strip '#' from color."""
        return self.hex_color[1:]


def read_file(input_file):
    """Read data from a file and trim newlines."""
    with open(input_file, "r") as file:
        return file.read().splitlines()


def read_file_json(input_file):
    """Read data from a json file."""
    with open(input_file, "r") as json_file:
        return json.load(json_file)


def read_file_raw(input_file):
    """Read data from a file as is, don't strip
       newlines or other special characters.."""
    with open(input_file, "r") as file:
        return file.readlines()


def save_file(data, export_file):
    """Write data to a file."""
    create_dir(os.path.dirname(export_file))

    try:
        with open(export_file, "w") as file:
            file.write(data)
    except PermissionError:
        logging.warning("Couldn't write to %s.", export_file)


def save_file_json(data, export_file):
    """Write data to a json file."""
    create_dir(os.path.dirname(export_file))

    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)


def create_dir(directory):
    """Alias to create the cache dir."""
    os.makedirs(directory, exist_ok=True)


def setup_logging():
    """Logging config."""
    logging.basicConfig(format=("[%(levelname)s\033[0m] "
                                "\033[1;31m%(module)s\033[0m: "
                                "%(message)s"),
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.addLevelName(logging.ERROR, '\033[1;31mE')
    logging.addLevelName(logging.INFO, '\033[1;32mI')
    logging.addLevelName(logging.WARNING, '\033[1;33mW')


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    return tuple(bytes.fromhex(color.strip("#")))


def hex_to_xrgba(color):
    """Convert a hex color to xrdb rgba."""
    col = color.lower().strip("#")
    return "%s%s/%s%s/%s%s/ff" % (*col,)


def rgb_to_hex(color):
    """Convert an rgb color to hex."""
    return "#%02x%02x%02x" % (*color,)


def darken_color(color, amount):
    """Darken a hex color."""
    color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def lighten_color(color, amount):
    """Lighten a hex color."""
    color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def blend_color(color, color2):
    """Blend two colors together."""
    r1, g1, b1 = hex_to_rgb(color)
    r2, g2, b2 = hex_to_rgb(color2)

    r3 = int(0.5 * r1 + 0.5 * r2)
    g3 = int(0.5 * g1 + 0.5 * g2)
    b3 = int(0.5 * b1 + 0.5 * b2)

    return rgb_to_hex((r3, g3, b3))


def saturate_color(color, amount):
    """Saturate a hex color."""
    r, g, b = hex_to_rgb(color)
    r, g, b = [x/255.0 for x in (r, g, b)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s = amount
    v = 0.2
    r, g, b = colorsys.hls_to_rgb(h, s, v)
    r, g, b = [x*255.0 for x in (r, g, b)]

    return rgb_to_hex((int(r), int(g), int(b)))


def rgb_to_yiq(color):
    """Sort a list of colors."""
    return colorsys.rgb_to_yiq(*hex_to_rgb(color))


def disown(cmd):
    """Call a system command in the background,
       disown it and hide it's output."""
    subprocess.Popen(cmd,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
