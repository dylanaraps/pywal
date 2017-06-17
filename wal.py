"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps
"""
import argparse
import re
import subprocess
import random

import os
from os.path import expanduser

import pathlib
from pathlib import Path


# Internal variables.
CACHE_DIR = expanduser("~") + "/.cache/wal"
COLOR_COUNT = 16
OS = os.uname


def get_args():
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

    # Add the args.
    arg.add_argument('-a', metavar='0-100', type=int,
                     help='Set terminal background transparency. \
                           *Only works in URxvt*')

    arg.add_argument('-c', action='store_true',
                     help='Delete all cached colorschemes.')

    arg.add_argument('-f', metavar='"/path/to/colors"',
                     help='Load colors directly from a colorscheme file.')

    arg.add_argument('-i', metavar='"/path/to/img.jpg"', required=True,
                     help='Which image or directory to use.')

    arg.add_argument('-n', action='store_true',
                     help='Skip setting the wallpaper.')

    arg.add_argument('-o', metavar='script_name',
                     help='External script to run after "wal".')

    arg.add_argument('-q', action='store_true',
                     help='Quiet mode, don\'t print anything.')

    arg.add_argument('-r', action='store_true',
                     help='Reload current colorscheme.')

    arg.add_argument('-t', action='store_true',
                     help='Fix artifacts in VTE Terminals. \
                           (Termite, xfce4-terminal)')

    arg.add_argument('-x', action='store_true',
                     help='Use extended 16-color palette.')

    return arg.parse_args()


def get_image(img):
    """Validate image input."""
    image = Path(img)

    if image.is_file():
        return image

    elif image.is_dir():
        rand = random.choice(os.listdir(image))
        rand_img = Path(str(image) + "/" + rand)

        if rand_img.is_file():
            return rand_img


def get_colors(img):
    """Generate a colorscheme using imagemagick."""
    colors = []

    # Create colorscheme dir.
    pathlib.Path(CACHE_DIR + "/schemes").mkdir(parents=True, exist_ok=True)

    # Cache file.
    cache_file = CACHE_DIR + "/schemes/" + img.replace('/', '_')

    # Cache the wallpaper name.
    wal = open(CACHE_DIR + "/wal", 'w')
    wal.write(img + "\n")
    wal.close()

    # Long-ass imagemagick command.
    magic = subprocess.Popen(["convert", img, "+dither", "-colors",
                              str(COLOR_COUNT), "-unique-colors", "txt:-"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    # Create a list of hex colors.
    for color in magic.stdout:
        hex_color = re.search('#.{6}', str(color))

        if hex_color:
            colors.append(hex_color.group(0))

    # Remove the first element, which isn't a color.
    del colors[0]

    # Cache the colorscheme.
    scheme = open(cache_file, 'w')
    for color in colors:
        scheme.write(color + "\n")
    scheme.close()


def main():
    """Main script function."""
    args = get_args()
    image = str(get_image(args.i))
    get_colors(image)
    return 0


main()
