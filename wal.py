#!/usr/bin/env python
#
# wal - Generate and change colorschemes on the fly.
#
# Created by Dylan Araps

import argparse
import os
import pathlib
import subprocess
import re
from pathlib import Path
from os.path import expanduser

# Internal variables.
cache_dir = expanduser("~") + "/.cache/wal"
color_count = 16
os = os.uname


def get_args():
    parser = argparse.ArgumentParser(description='wal - Generate colorschemes on the fly')

    parser.add_argument('-a', help='Set terminal background transparency. *Only works in URxvt*', metavar='0-100', type=int)
    parser.add_argument('-c', help='Delete all cached colorschemes.', action='store_true')
    parser.add_argument('-f', help='Load colors directly from a colorscheme file.', metavar='"/path/to/colors"')
    parser.add_argument('-i', help='Which image or directory to use.', metavar='"/path/to/img.jpg"')
    parser.add_argument('-n', help='Skip setting the wallpaper.', action='store_true')
    parser.add_argument('-o', help='External script to run after "wal".', metavar='script_name')
    parser.add_argument('-q', help='Quiet mode, don\'t print anything.', action='store_true')
    parser.add_argument('-r', help='Reload current colorscheme.', action='store_true')
    parser.add_argument('-t', help='Fix artifacts in VTE Terminals. (Termite, xfce4-terminal)', action='store_true')
    parser.add_argument('-x', help='Use extended 16-color palette.', action='store_true')

    return parser.parse_args()


def get_colors(img):
    image = Path(img)

    if image.is_file():
        colors = []

        # Create colorscheme dir.
        pathlib.Path(cache_dir + "/schemes").mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir + "/schemes/" + img.replace('/', '_')

        # Cache the wallpaper name.
        wal = open(cache_dir + "/wal", 'w')
        wal.write(img)
        wal.close()

        # Long-ass imagemagick command.
        magic = subprocess.Popen(["convert", img, "+dither", "-colors",
                str(color_count), "-unique-colors", "txt:-"],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)


        # Create a list of hex colors.
        for color in magic.stdout:
            print(color)
            hex = re.search('#.{6}', str(color))

            if hex:
                colors.append(hex.group(0))


        # Remove the first element which isn't a color.
        del colors[0]

        # Cache the colorscheme.
        scheme = open(cache_file, 'w')

        for color in colors:
            scheme.write(color + "\n")

        scheme.close()


def main():
    args = get_args()
    get_colors(args.i)
    return 0


main()
