"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps
"""
import argparse
import re
import random
import glob
import shutil

import subprocess
from subprocess import call

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


def magic(color_count, img):
    """Call Imagemagick to generate a scheme."""
    colors = subprocess.Popen(["convert", img, "+dither", "-colors",
                               str(color_count), "-unique-colors", "txt:-"],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    return colors.stdout


def gen_colors(img):
    """Generate a color palette using imagemagick."""
    colors = []

    # Generate initial scheme.
    magic_output = magic(COLOR_COUNT, img).readlines()

    # If imagemagick finds less than 16 colors, use a larger source number
    # of colors.
    index = 0
    while len(magic_output) - 1 <= 15:
        index += 1
        magic_output = magic(COLOR_COUNT + index, img).readlines()

        print("colors: Imagemagick couldn't generate a", COLOR_COUNT,
              "color palette, trying a larger palette size",
              COLOR_COUNT + index)

    # Create a list of hex colors.
    for color in magic_output:
        hex_color = re.search('#.{6}', str(color))

        if hex_color:
            colors.append(hex_color.group(0))

    # Remove the first element, which isn't a color.
    del colors[0]

    return colors


def get_colors(img):
    """Generate a colorscheme using imagemagick."""
    # Cache file.
    cache_file = Path(CACHE_DIR + "/schemes/" + img.replace('/', '_'))

    if cache_file.is_file():
        with open(cache_file) as file:
            colors = file.readlines()

        colors = [x.strip() for x in colors]
    else:
        # Cache the wallpaper name.
        wal = open(CACHE_DIR + "/wal", 'w')
        wal.write(img + "\n")
        wal.close()

        # Generate the colors.
        colors = gen_colors(img)

        # Cache the colorscheme.
        scheme = open(cache_file, 'w')
        for color in colors:
            scheme.write(color + "\n")
        scheme.close()

    print("colors: Generated colorscheme")
    return colors


def set_special(index, color):
    """Build the escape sequence for special colors."""
    return "\\033]" + str(index) + ";" + color + "\\007"


def set_color(index, color):
    """Build the escape sequence we need for each color."""
    return "\\033]4;" + str(index) + ";" + color + "\\007"


def send_sequences(colors, vte):
    """Send colors to all open terminals."""
    sequences = set_special(10, colors[15])
    sequences += set_special(11, colors[0])
    sequences += set_special(12, colors[15])
    sequences += set_special(13, colors[15])
    sequences += set_special(14, colors[0])

    # This escape sequence doesn't work in VTE terminals.
    if not vte:
        sequences += set_special(708, colors[0])

    sequences += set_color(0, colors[0])
    sequences += set_color(1, colors[9])
    sequences += set_color(2, colors[10])
    sequences += set_color(3, colors[11])
    sequences += set_color(4, colors[12])
    sequences += set_color(5, colors[13])
    sequences += set_color(6, colors[14])
    sequences += set_color(7, colors[15])
    sequences += set_color(9, colors[9])
    sequences += set_color(10, colors[10])
    sequences += set_color(11, colors[11])
    sequences += set_color(12, colors[12])
    sequences += set_color(13, colors[13])
    sequences += set_color(14, colors[14])
    sequences += set_color(15, colors[15])

    # Hardcode color 8 to a grey color.
    brightness = int(colors[0][1])

    if 0 <= brightness <= 1:
        sequences += set_color(8, "#666666")

    elif brightness == 2:
        sequences += set_color(8, "#757575")

    elif 3 <= brightness <= 4:
        sequences += set_color(8, "#999999")

    elif brightness == 5:
        sequences += set_color(8, "#8a8a8a")

    elif 6 <= brightness <= 9:
        sequences += set_color(8, "#a1a1a1")

    else:
        sequences += set_color(8, colors[7])

    # Set a blank color that isn't affected by bold highlighting.
    sequences += set_color(66, colors[0])

    # Decode the string.
    sequences = bytes(sequences, "utf-8").decode("unicode_escape")

    # Send the sequences to all open terminals.
    for term in glob.glob("/dev/pts/[0-9]*"):
        term_file = open(term, 'w')
        term_file.write(sequences)
        term_file.close()

    print("colors: Set terminal colors")


def set_wallpaper(img):
    """Set the wallpaper."""
    if shutil.which("feh"):
        call(["feh", "--bg-fill", img])

    elif shutil.which("nitrogen"):
        call(["nitrogen", "--set-zoom-fill", img])

    elif shutil.which("bgs"):
        call(["bgs", img])

    elif shutil.which("hsetroot"):
        call(["hsetroot", "-fill", img])

    elif shutil.which("habak"):
        call(["habak", "-mS", img])

    elif OS == "Darwin":
        call(["osascript", "-e", "'tell application \"Finder\" to set \
              desktop picture to POSIX file\'", img, "\'"])

    else:
        call(["gsettings", "set", "org.gnome.desktop.background",
              "picture-uri", img])

    print("wallpaper: Set the new wallpaper")
    return 0


def main():
    """Main script function."""
    args = get_args()
    image = str(get_image(args.i))

    # Create colorscheme dir.
    pathlib.Path(CACHE_DIR + "/schemes").mkdir(parents=True, exist_ok=True)

    colors = get_colors(image)
    send_sequences(colors, args.t)
    set_wallpaper(image)

    return 0


main()
