"""
                                      '||
... ...  .... ... ... ... ...  ....    ||
 ||'  ||  '|.  |   ||  ||  |  '' .||   ||
 ||    |   '|.|     ||| |||   .|' ||   ||
 ||...'     '|       |   |    '|..'|' .||.
 ||      .. |
''''      ''
Created by Dylan Araps.
"""

import argparse
import os
import shutil
import sys

from .settings import __version__, CACHE_DIR
from . import colors
from . import export
from . import image
from . import reload
from . import sequences
from . import util
from . import wallpaper


def get_args(args):
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("-a", metavar="\"alpha\"",
                     help="Set terminal background transparency. \
                           *Only works in URxvt*")

    arg.add_argument("-b", metavar="background",
                     help="Custom background color to use.")

    arg.add_argument("-c", action="store_true",
                     help="Delete all cached colorschemes.")

    arg.add_argument("-i", metavar="\"/path/to/img.jpg\"",
                     help="Which image or directory to use.")

    arg.add_argument("-f", metavar="\"/path/to/colorscheme/file\"",
                     help="Which colorscheme file to use.")

    arg.add_argument("-g", action="store_true",
                     help="Generate an oomox theme.")

    arg.add_argument("-n", action="store_true",
                     help="Skip setting the wallpaper.")

    arg.add_argument("-o", metavar="\"script_name\"",
                     help="External script to run after \"wal\".")

    arg.add_argument("-q", action="store_true",
                     help="Quiet mode, don\'t print anything and \
                           don't display notifications.")

    arg.add_argument("-r", action="store_true",
                     help="'wal -r' is deprecated: Use \
                           (cat ~/.cache/wal/sequences &) instead.")

    arg.add_argument("-R", action="store_true",
                     help="Restore previous colorscheme.")

    arg.add_argument("-s", action="store_true",
                     help="Skip changing colors in terminals.")

    arg.add_argument("-t", action="store_false",
                     help="Deprecated: Does nothing and is no longer needed.")

    arg.add_argument("-v", action="store_true",
                     help="Print \"wal\" version.")

    arg.add_argument("-e", action="store_true",
                     help="Skip reloading gtk/xrdb/i3/sway/polybar")

    return arg.parse_args(args)


def process_args(args):
    """Process args."""
    if not len(sys.argv) > 1:
        print("error: wal needs to be given arguments to run.\n"
              "       Refer to \"wal -h\" for more info.")
        sys.exit(1)

    if args.i and args.f:
        print("error: Conflicting arguments -i and -f.\n"
              "       Refer to \"wal -h\" for more info.")
        sys.exit(1)

    if args.v:
        print("wal", __version__)
        sys.exit(0)

    if args.r:
        reload.colors()
        sys.exit(0)

    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if args.c:
        scheme_dir = os.path.join(CACHE_DIR, "schemes")
        shutil.rmtree(scheme_dir, ignore_errors=True)

    if args.R:
        image_file = os.path.join(CACHE_DIR, "wal")

        if os.path.isfile(image_file):
            args.i = util.read_file(image_file)[0]
        else:
            print("image: No colorscheme to restore, try 'wal -i' first.")
            sys.exit(1)

    if args.i:
        image_file = image.get(args.i)
        colors_plain = colors.get(image_file, notify=not args.q)

    if args.f:
        colors_plain = colors.file(args.f)

    if args.a:
        util.Color.alpha_num = args.a

    if args.b:
        args.b = "#%s" % (args.b.strip("#"))
        colors_plain["special"]["background"] = args.b
        colors_plain["colors"]["color0"] = args.b

    if args.i or args.f:
        if not args.n:
            wallpaper.change(colors_plain["wallpaper"])

        if not args.s:
            sequences.send(colors_plain)

        export.every(colors_plain)

        if not args.e:
            reload.env()

    if args.o:
        util.disown([args.o])

    if not args.e:
        reload.oomox(args.g)
        reload.gtk()


def main():
    """Main script function."""
    args = get_args(sys.argv[1:])
    process_args(args)


if __name__ == "__main__":
    main()
