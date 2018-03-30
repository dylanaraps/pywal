"""
Generate a colorscheme using ColorThief.
"""
import sys

from colorthief import ColorThief

from .. import util


def gen_colors(img):
    """Loop until 16 colors are generated."""
    color_cmd = ColorThief(img).get_palette

    for i in range(0, 20, 1):
        raw_colors = color_cmd(color_count=16 + i)

        if len(raw_colors) > 16:
            break

        elif i == 19:
            print("colors: ColorThief couldn't generate a suitable palette",
                  "for the image. Exiting...")
            sys.exit(1)

        else:
            print("colors: ColorThief couldn't create a suitable palette, "
                  "trying a larger palette size", 16 + i)

    return [util.rgb_to_hex(color) for color in raw_colors]


def adjust(img, colors, light):
    """Create palette."""
    if light:
        print("colors: Colortheif backend doesn't support light themes.")

    raw_colors = colors[:1] + colors[8:16] + colors[8:-1]

    raw_colors[0] = util.darken_color(colors[0], 0.80)
    raw_colors[15] = util.lighten_color(colors[15], 0.80)
    raw_colors[7] = raw_colors[15]

    colors = {"wallpaper": img,
              "alpha": util.Color.alpha_num,
              "special": {},
              "colors": {}}

    for i, color in enumerate(raw_colors):
        colors["colors"]["color%s" % i] = util.lighten_color(color, 0.25)

    raw_colors[8] = util.blend_color(raw_colors[0], raw_colors[15])

    colors["colors"]["color0"] = raw_colors[0]
    colors["special"]["background"] = raw_colors[0]
    colors["special"]["foreground"] = raw_colors[15]
    colors["special"]["cursor"] = raw_colors[1]

    return colors


def get(img, light=False):
    """Get colorscheme."""
    colors = gen_colors(img)
    return adjust(img, colors, light)
