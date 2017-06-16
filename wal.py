#!/usr/bin/env python
#
# wal - Generate and change colorschemes on the fly.
#
# Created by Dylan Araps

import argparse
import os
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
        print("File exists!")
    else:
        print("File doesn't exist. :(")


def main():
    args = get_args()
    get_colors(args.i)
    return 0


main()
