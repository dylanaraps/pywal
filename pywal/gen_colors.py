"""
Generate a colorscheme.
"""
import os
import pathlib
import random
import re
import shutil
import subprocess

from pywal.settings import CACHE_DIR, COLOR_COUNT
from pywal import util


def random_img(img_dir):
    """Pick a random image file from a directory."""
    current_wall = pathlib.Path(CACHE_DIR / "wal")

    if current_wall.is_file():
        current_wall = util.read_file(current_wall)
        current_wall = os.path.basename(current_wall[0])

    # Add all images to a list excluding the current wallpaper.
    file_types = (".png", ".jpg", ".jpeg", ".jpe", ".gif")
    images = [img for img in os.listdir(img_dir)
              if img.endswith(file_types) and img != current_wall]

    return pathlib.Path(img_dir / random.choice(images))


def get_image(img):
    """Validate image input."""
    image = pathlib.Path(img)

    if image.is_file():
        wal_img = image

    elif image.is_dir():
        wal_img = random_img(image)

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
    # Check if the user has Imagemagick installed.
    if not shutil.which("convert"):
        print("error: imagemagick not found, exiting...\n"
              "error: wal requires imagemagick to function.")
        exit(1)

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


def get_colors(img, quiet):
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
        if not quiet:
            util.disown("notify-send", "wal: Generating a colorscheme...")

        # Generate the colors.
        colors = gen_colors(img)
        colors = sort_colors(colors)

        # Cache the colorscheme.
        util.save_file("\n".join(colors), cache_file)

        print("colors: Generated colorscheme")
        if not quiet:
            util.disown("notify-send", "wal: Generation complete.")

    return colors


def sort_colors(colors):
    """Sort the generated colors."""
    return colors[:1] + colors[9:] + colors[8:]
