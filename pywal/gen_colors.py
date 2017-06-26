"""
Generate a colorscheme.
"""
import os
import pathlib
import random
import re
import shutil
import subprocess

from pywal import settings as s
from pywal import set_colors
from pywal import util


CACHE_DIR = s.CACHE_DIR
COLOR_COUNT = s.COLOR_COUNT


def get_image(img):
    """Validate image input."""
    # Check if the user has Imagemagick installed.
    if not shutil.which("convert"):
        print("error: imagemagick not found, exiting...\n"
              "error: wal requires imagemagick to function.")
        exit(1)

    image = pathlib.Path(img)

    if image.is_file():
        wal_img = image

    # Pick a random image from the directory.
    elif image.is_dir():
        file_types = (".png", ".jpg", ".jpeg", ".jpe", ".gif")

        # Get the filename of the current wallpaper.
        current_img = pathlib.Path(CACHE_DIR / "wal")

        if current_img.is_file():
            current_img = util.read_file(current_img)
            current_img = os.path.basename(current_img[0])

        # Get a list of images.
        images = [img for img in os.listdir(image)
                  if img.endswith(file_types) and
                  img != current_img]

        wal_img = random.choice(images)
        wal_img = pathlib.Path(image / wal_img)

    else:
        print("error: No valid image file found.")
        exit(1)

    print("image: Using image", wal_img)
    return str(wal_img)


def imagemagick(color_count, img):
    """Call Imagemagick to generate a scheme."""
    colors = subprocess.Popen(["convert", img, "+dither", "-colors",
                               str(color_count), "-unique-colors", "txt:-"],
                              stdout=subprocess.PIPE)

    return colors.stdout.readlines()


def gen_colors(img):
    """Generate a color palette using imagemagick."""
    # Generate initial scheme.
    raw_colors = imagemagick(COLOR_COUNT, img)

    # If imagemagick finds less than 16 colors, use a larger source number
    # of colors.
    index = 0
    while len(raw_colors) - 1 < COLOR_COUNT:
        index += 1
        raw_colors = imagemagick(COLOR_COUNT + index, img)

        print("colors: Imagemagick couldn't generate a", COLOR_COUNT,
              "color palette, trying a larger palette size",
              COLOR_COUNT + index)

    # Remove the first element, which isn't a color.
    del raw_colors[0]

    # Create a list of hex colors.
    return [re.search("#.{6}", str(col)).group(0) for col in raw_colors]


def get_colors(img):
    """Generate a colorscheme using imagemagick."""
    # Cache the wallpaper name.
    util.save_file(img, CACHE_DIR / "wal")

    # Cache the sequences file.
    cache_file = pathlib.Path(CACHE_DIR / "schemes" / img.replace("/", "_"))

    if cache_file.is_file():
        colors = util.read_file(cache_file)
        print("colors: Found cached colorscheme.")

    else:
        print("colors: Generating a colorscheme...")
        util.notify("wal: Generating a colorscheme...")

        # Generate the colors.
        colors = gen_colors(img)
        colors = sort_colors(colors)

        # Cache the colorscheme.
        util.save_file("\n".join(colors), cache_file)

        print("colors: Generated colorscheme")
        util.notify("wal: Generation complete.")

    return colors


def sort_colors(colors):
    """Sort the generated colors."""
    sorted_colors = []
    sorted_colors.append(colors[0])
    sorted_colors.append(colors[9])
    sorted_colors.append(colors[10])
    sorted_colors.append(colors[11])
    sorted_colors.append(colors[12])
    sorted_colors.append(colors[13])
    sorted_colors.append(colors[14])
    sorted_colors.append(colors[15])
    sorted_colors.append(set_colors.set_grey(colors))
    sorted_colors.append(colors[9])
    sorted_colors.append(colors[10])
    sorted_colors.append(colors[11])
    sorted_colors.append(colors[12])
    sorted_colors.append(colors[13])
    sorted_colors.append(colors[14])
    sorted_colors.append(colors[15])
    return sorted_colors


def reload_colors(vte):
    """Reload colors."""
    sequence_file = pathlib.Path(CACHE_DIR / "sequences")

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the problem sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        # Make the terminal interpret escape sequences.
        print(util.fix_escape(sequences), end="")

    exit(0)
