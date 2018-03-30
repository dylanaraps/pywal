"""
Generate a colorscheme using ColorThief.
"""
import sys

from colorthief import ColorThief

from .. import util
from ..settings import COLOR_COUNT


def adjust(img, colors):
    """Create palette."""
    raw_colors = colors[:1] + colors[8:16] + colors[8:-1]

    # Modify colors to make a better scheme.
    raw_colors[0] = util.darken_color(colors[0], 0.80)
    raw_colors[15] = util.lighten_color(colors[15], 0.80)
    raw_colors[7] = raw_colors[15]

    colors = {"wallpaper": img, "alpha": util.Color.alpha_num,
              "special": {}, "colors": {}}

    for i, color in enumerate(raw_colors):
        colors["colors"]["color%s" % i] = util.lighten_color(color, 0.25)

    raw_colors[8] = util.blend_color(raw_colors[0], raw_colors[15])

    colors["colors"]["color0"] = raw_colors[0]
    colors["special"]["background"] = raw_colors[0]
    colors["special"]["foreground"] = raw_colors[15]
    colors["special"]["cursor"] = raw_colors[1]

    return colors


def gen_colors(img, color_count):
    """Loop until 16 colors are generated."""
    color_thief = ColorThief(img)
    color_cmd = color_thief.get_palette

    for i in range(0, 20, 1):
        raw_colors = color_cmd(color_count=color_count + i)

        if len(raw_colors) > 16:
            break

        elif i == 19:
            print("colors: ColorThief couldn't generate a suitable scheme",
                  "for the image. Exiting...")
            sys.exit(1)

        else:
            print("colors: ColorThief couldn't generate a %s color palette, "
                  "trying a larger palette size %s."
                  % (color_count, color_count + i))

    return [util.rgb_to_hex(color) for color in raw_colors]


def get(img, color_count=COLOR_COUNT, light=False):
    """Get colorscheme."""
    colors = gen_colors(img, color_count)
    return adjust(img, colors)
