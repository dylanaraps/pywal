"""
Generate a colorscheme using ColorThief.
"""
import sys

from colorthief import ColorThief

from .. import util


def gen_colors(img):
    """Loop until 16 colors are generated."""
    color_cmd = ColorThief(img).get_palette

    for i in range(0, 10, 1):
        raw_colors = color_cmd(color_count=8 + i)

        if len(raw_colors) >= 8:
            break

        elif i == 19:
            print("colors: ColorThief couldn't generate a suitable palette",
                  "for the image. Exiting...")
            sys.exit(1)

        else:
            print("colors: ColorThief couldn't create a suitable palette, "
                  "trying a larger palette size", 8 + i)

    return [util.rgb_to_hex(color) for color in raw_colors]


def adjust(colors, light):
    """Create palette."""
    colors.sort(key=util.rgb_to_yiq)
    raw_colors = [*colors, *colors]

    if light:
        raw_colors[0] = util.lighten_color(colors[0], 0.90)
        raw_colors[7] = util.darken_color(colors[0], 0.75)

    else:
        for color in raw_colors:
            color = util.lighten_color(color, 0.40)

        raw_colors[0] = util.darken_color(colors[0], 0.80)
        raw_colors[7] = util.lighten_color(colors[0], 0.60)

    raw_colors[8] = util.lighten_color(colors[0], 0.20)
    raw_colors[15] = raw_colors[7]

    return raw_colors


def get(img, light=False):
    """Get colorscheme."""
    colors = gen_colors(img)
    return adjust(colors, light)
