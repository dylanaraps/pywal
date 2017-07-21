"""
Generate a colorscheme using imagemagick.
"""
import re
import shutil
import subprocess

# from pywal.settings import color_count
from pywal import util


def imagemagick(color_count, img):
    """Call Imagemagick to generate a scheme."""
    colors = subprocess.Popen(["convert", img, "+dither", "-colors",
                               str(color_count), "-unique-colors", "txt:-"],
                              stdout=subprocess.PIPE)

    return colors.stdout.readlines()


def gen_colors(img, color_count):
    """Format the output from imagemagick into a list
       of hex colors."""
    # Check if the user has Imagemagick installed.
    if not shutil.which("convert"):
        print("error: imagemagick not found, exiting...\n"
              "error: wal requires imagemagick to function.")
        exit(1)

    # Generate initial scheme.
    raw_colors = imagemagick(color_count, img)

    # If imagemagick finds less than 16 colors, use a larger source number
    # of colors.
    index = 0
    while len(raw_colors) - 1 < color_count:
        index += 1
        raw_colors = imagemagick(color_count + index, img)

        print("colors: Imagemagick couldn't generate a", color_count,
              "color palette, trying a larger palette size",
              color_count + index)

        if index > 20:
            print("colors: Imagemagick couldn't generate a suitable scheme",
                  "for the image. Exiting...")
            quit(1)

    # Remove the first element, which isn't a color.
    del raw_colors[0]

    # Create a list of hex colors.
    return [re.search("#.{6}", str(col)).group(0) for col in raw_colors]


def get_colors(img, cache_dir, color_count, quiet):
    """Get the colorscheme."""
    # Cache the wallpaper name.
    util.save_file(img, cache_dir / "wal")

    # Cache the sequences file.
    # _home_dylan_img_jpg.json
    cache_file = cache_dir / "schemes" / \
        img.replace("/", "_").replace(".", "_")
    cache_file = cache_file.with_suffix(".json")

    if cache_file.is_file():
        colors = util.read_file_json(cache_file)
        print("colors: Found cached colorscheme.")

    else:
        util.msg("wal: Generating a colorscheme...", quiet)

        # Generate the colors.
        colors = gen_colors(img, color_count)
        colors = sort_colors(img, colors)

        # Cache the colorscheme.
        util.save_file_json(colors, cache_file)
        util.msg("wal: Generation complete.", quiet)

    return colors


def sort_colors(img, colors):
    """Sort the generated colors and store them in a dict that
       we will later save in json format."""
    raw_colors = colors[:1] + colors[9:] + colors[8:]

    # Wallpaper.
    colors = {"wallpaper": img}

    # Special colors.
    colors_special = {}
    colors_special.update({"background": raw_colors[0]})
    colors_special.update({"foreground": raw_colors[15]})
    colors_special.update({"cursor": raw_colors[15]})

    # Colors 0-15.
    colors_hex = {}
    [colors_hex.update({f"color{index}": color})  # pylint: disable=W0106
     for index, color in enumerate(raw_colors)]

    # Color 8.
    colors_hex["color8"] = util.set_grey(raw_colors)

    # Add the colors to a dict.
    colors["special"] = colors_special
    colors["colors"] = colors_hex

    return colors
