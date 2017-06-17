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
from subprocess import Popen

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

    arg.add_argument('-i', metavar='"/path/to/img.jpg"',
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


def reload_colors():
    """Reload colors."""
    with open(CACHE_DIR + "/sequences") as file:
        sequences = file.read()

    # Decode the string.
    sequences = bytes(sequences, "utf-8").decode("unicode_escape")

    print(sequences, end='')
    quit()


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
    colors = Popen(["convert", img, "+dither", "-colors",
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


def get_grey(color, color2):
    """Set a grey color based on brightness of color0"""
    brightness = int(color[1])

    if 0 <= brightness <= 1:
        return "#666666"

    elif brightness == 2:
        return "#757575"

    elif 3 <= brightness <= 4:
        return "#999999"

    elif brightness == 5:
        return "#8a8a8a"

    elif 6 <= brightness <= 9:
        return "#a1a1a1"

    return color2


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
    sequences += set_color(8, get_grey(colors[0], colors[7]))
    sequences += set_color(9, colors[9])
    sequences += set_color(10, colors[10])
    sequences += set_color(11, colors[11])
    sequences += set_color(12, colors[12])
    sequences += set_color(13, colors[13])
    sequences += set_color(14, colors[14])
    sequences += set_color(15, colors[15])

    # Set a blank color that isn't affected by bold highlighting.
    sequences += set_color(66, colors[0])

    # Decode the string.
    sequences = bytes(sequences, "utf-8").decode("unicode_escape")

    # Send the sequences to all open terminals.
    for term in glob.glob("/dev/pts/[0-9]*"):
        term_file = open(term, 'w')
        term_file.write(sequences)
        term_file.close()

    # Cache the sequences.
    sequence_file = open(CACHE_DIR + "/sequences", 'w')
    sequence_file.write(sequences)
    sequence_file.close()

    print("colors: Set terminal colors")


def set_wallpaper(img):
    """Set the wallpaper."""
    if shutil.which("feh"):
        Popen(["feh", "--bg-fill", img])

    elif shutil.which("nitrogen"):
        Popen(["nitrogen", "--set-zoom-fill", img])

    elif shutil.which("bgs"):
        Popen(["bgs", img])

    elif shutil.which("hsetroot"):
        Popen(["hsetroot", "-fill", img])

    elif shutil.which("habak"):
        Popen(["habak", "-mS", img])

    elif OS == "Darwin":
        Popen(["osascript", "-e", "'tell application \"Finder\" to set \
              desktop picture to POSIX file\'", img, "\'"])

    else:
        Popen(["gsettings", "set", "org.gnome.desktop.background",
               "picture-uri", img])

    print("wallpaper: Set the new wallpaper")
    return 0


def export_plain(colors):
    """Export colors to a plain text file."""
    plain_file = CACHE_DIR + "/" + "colors"

    file = open(plain_file, 'w')
    for color in colors:
        file.write(color + "\n")
    file.close()


def export_xrdb(colors):
    """Export colors to xrdb."""
    x_colors = "URxvt*foreground: " + colors[15] + "\n"
    x_colors += "XTerm*foreground: " + colors[15] + "\n"
    x_colors += "URxvt*background: " + colors[0] + "\n"
    x_colors += "XTerm*background: " + colors[0] + "\n"
    x_colors += "URxvt*cursorColor: " + colors[15] + "\n"
    x_colors += "XTerm*cursorColor: " + colors[15] + "\n"
    x_colors += "*.color0: " + colors[0] + "\n"
    x_colors += "*.color1: " + colors[9] + "\n"
    x_colors += "*.color2: " + colors[10] + "\n"
    x_colors += "*.color3: " + colors[11] + "\n"
    x_colors += "*.color4: " + colors[12] + "\n"
    x_colors += "*.color5: " + colors[13] + "\n"
    x_colors += "*.color6: " + colors[14] + "\n"
    x_colors += "*.color7: " + colors[15] + "\n"
    x_colors += "*.color8: " + get_grey(colors[0], colors[7]) + "\n"
    x_colors += "*.color9: " + colors[9] + "\n"
    x_colors += "*.color10: " + colors[10] + "\n"
    x_colors += "*.color11: " + colors[11] + "\n"
    x_colors += "*.color12: " + colors[12] + "\n"
    x_colors += "*.color13: " + colors[13] + "\n"
    x_colors += "*.color14: " + colors[14] + "\n"
    x_colors += "*.color15: " + colors[15] + "\n"

    xrdb_file = CACHE_DIR + "/" + "xcolors"

    file = open(xrdb_file, 'w')
    file.write(x_colors)
    file.close()

    # Merge the colors into the X db so new terminals use them.
    call(["xrdb", "-merge", "<<<", xrdb_file])

    print("export: Exported xrdb colors.")


def main():
    """Main script function."""
    args = get_args()

    if args.r:
        reload_colors()

    image = str(get_image(args.i))

    # Create colorscheme dir.
    pathlib.Path(CACHE_DIR + "/schemes").mkdir(parents=True, exist_ok=True)

    # Get the colors.
    colors = get_colors(image)

    # Set the colors.
    send_sequences(colors, args.t)
    set_wallpaper(image)
    export_plain(colors)
    export_xrdb(colors)

    return 0


main()
