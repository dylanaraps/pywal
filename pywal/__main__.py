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
import logging
import os
import shutil
import sys

from .settings import __version__, CACHE_DIR, CONF_DIR
from . import colors
from . import export
from . import image
from . import reload
from . import sequences
from . import theme
from . import util
from . import wallpaper


def get_args():
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("-a", metavar="\"alpha\"",
                     help="Set terminal background transparency. \
                           *Only works in URxvt*")

    arg.add_argument("-b", metavar="background",
                     help="Custom background color to use.")

    arg.add_argument("--backend", metavar="backend",
                     help="Which color backend to use. \
                           Use 'wal --backend' to list backends.",
                     const="list_backends", type=str, nargs="?")

    arg.add_argument("--theme", "-f", metavar="/path/to/file or theme_name",
                     help="Which colorscheme file to use. \
                           Use 'wal --theme' to list builtin themes.",
                     const="list_themes", nargs="?")

    arg.add_argument("--iterative", action="store_true",
                     help="When pywal is given a directory as input and this "
                          "flag is used: Go through the images in order "
                          "instead of shuffled.")

    arg.add_argument("--saturate", metavar="0.0-1.0",
                     help="Set the color saturation.")

    arg.add_argument("--preview", action="store_true",
                     help="Print the current color palette.")

    arg.add_argument("-c", action="store_true",
                     help="Delete all cached colorschemes.")

    arg.add_argument("-i", metavar="\"/path/to/img.jpg\"",
                     help="Which image or directory to use.")

    arg.add_argument("-g", action="store_true",
                     help="Generate an oomox theme.")

    arg.add_argument("-l", action="store_true",
                     help="Generate a light colorscheme.")

    arg.add_argument("-n", action="store_true",
                     help="Skip setting the wallpaper.")

    arg.add_argument("-o", metavar="\"script_name\"", action="append",
                     help="External script to run after \"wal\".")

    arg.add_argument("-q", action="store_true",
                     help="Quiet mode, don\'t print anything.")

    arg.add_argument("-r", action="store_true",
                     help="'wal -r' is deprecated: Use \
                           (cat ~/.cache/wal/sequences &) instead.")

    arg.add_argument("-R", action="store_true",
                     help="Restore previous colorscheme.")

    arg.add_argument("-s", action="store_true",
                     help="Skip changing colors in terminals.")

    arg.add_argument("-t", action="store_true",
                     help="Skip changing colors in tty.")

    arg.add_argument("-v", action="store_true",
                     help="Print \"wal\" version.")

    arg.add_argument("-e", action="store_true",
                     help="Skip reloading gtk/xrdb/i3/sway/polybar")

    return arg


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.v:
        parser.exit(0, "wal %s\n" % __version__)

    if args.preview:
        print("Current colorscheme:", sep='')
        colors.palette()
        sys.exit(0)

    if args.i and args.theme:
        parser.error("Conflicting arguments -i and -f.")

    if args.r:
        reload.colors()
        sys.exit(0)

    if args.c:
        scheme_dir = os.path.join(CACHE_DIR, "schemes")
        shutil.rmtree(scheme_dir, ignore_errors=True)
        sys.exit(0)

    if not args.i and \
       not args.theme and \
       not args.R and \
       not args.backend:
        parser.error("No input specified.\n"
                     "--backend, --theme, -i or -R are required.")

    if args.theme == "list_themes":
        theme.list_out()
        sys.exit(0)

    if args.backend == "list_backends":
        print("\n - ".join(["\033[1;32mBackends\033[0m:",
                            *colors.list_backends()]))
        sys.exit(0)


def parse_args(parser):
    """Process args."""
    args = parser.parse_args()

    if args.q:
        logging.getLogger().disabled = True
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if args.a:
        util.Color.alpha_num = args.a

    if args.i:
        image_file = image.get(args.i, iterative=args.iterative)
        colors_plain = colors.get(image_file, args.l, args.backend,
                                  sat=args.saturate)

    if args.theme:
        colors_plain = theme.file(args.theme, args.l)

    if args.R:
        colors_plain = theme.file(os.path.join(CACHE_DIR, "colors.json"))

    if args.b:
        args.b = "#%s" % (args.b.strip("#"))
        colors_plain["special"]["background"] = args.b
        colors_plain["colors"]["color0"] = args.b

    if not args.n:
        wallpaper.change(colors_plain["wallpaper"])

    sequences.send(colors_plain, to_send=not args.s)

    if sys.stdout.isatty():
        colors.palette()

    export.every(colors_plain)

    if not args.e:
        reload.env(tty_reload=not args.t)

    if args.o:
        for cmd in args.o:
            util.disown([cmd])

    if not args.e:
        reload.oomox(args.g)
        reload.gtk()


def main():
    """Main script function."""
    util.create_dir(os.path.join(CONF_DIR, "templates"))
    util.create_dir(os.path.join(CONF_DIR, "colorschemes/light/"))
    util.create_dir(os.path.join(CONF_DIR, "colorschemes/dark/"))

    util.setup_logging()
    parser = get_args()

    parse_args_exit(parser)
    parse_args(parser)


if __name__ == "__main__":
    main()
