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

from .settings import __version__, CACHE_DIR
from . import colors
from . import export
from . import image
from . import reload
from . import sequences
from . import theme
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

    arg.add_argument("--backend", metavar="backend",
                     help="Which color backend to use. \
                           Use 'wal --backend' to list backends.",
                     const="list_backends", type=str, nargs="?", default="wal")

    arg.add_argument("--theme", "-f", metavar="/path/to/file or theme_name",
                     help="Which colorscheme file to use. \
                           Use 'wal --theme' to list builtin themes.",
                     const="list_themes", nargs="?")

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

    arg.add_argument("-o", metavar="\"script_name\"",
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

    return arg.parse_args(args)


def process_args(args):
    """Process args."""
    if not len(sys.argv) > 1:
        print("error: wal needs to be given arguments to run.\n"
              "       Refer to \"wal -h\" for more info.")
        sys.exit(1)

    if args.i and args.theme:
        print("error: Conflicting arguments -i and -f.\n"
              "       Refer to \"wal -h\" for more info.")
        sys.exit(1)

    if args.v:
        print("wal", __version__)
        sys.exit(0)

    if args.r:
        reload.colors()
        sys.exit(0)

    if args.theme == "list_themes":
        themes = [theme.name.replace(".json", "")
                  for theme in theme.list_themes()]
        print("Themes:", themes)
        print("Extra: 'random' (select a random theme)")
        sys.exit(0)

    if args.backend == "list_backends":
        print("Backends:", colors.list_backends())
        sys.exit(0)

    if args.q:
        logging.getLogger().disabled = True
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if args.c:
        scheme_dir = os.path.join(CACHE_DIR, "schemes")
        shutil.rmtree(scheme_dir, ignore_errors=True)

    if args.i:
        image_file = image.get(args.i)
        colors_plain = colors.get(image_file, args.l, args.backend)

    if args.theme:
        colors_plain = theme.file(args.theme)

    if args.R:
        cache_file = os.path.join(CACHE_DIR, "colors.json")

        if os.path.isfile(cache_file):
            colors_plain = theme.file(cache_file)

        else:
            print("image: No colorscheme to restore, try 'wal -i' first.")
            sys.exit(1)

    if args.a:
        util.Color.alpha_num = args.a

    if args.b:
        args.b = "#%s" % (args.b.strip("#"))
        colors_plain["special"]["background"] = args.b
        colors_plain["colors"]["color0"] = args.b

    if args.i or args.theme or args.R:
        if not args.n:
            wallpaper.change(colors_plain["wallpaper"])

        sequences.send(colors_plain, to_send=not args.s)
        colors.palette()
        export.every(colors_plain)

        if not args.e:
            reload.env(tty_reload=not args.t)

    if args.o:
        util.disown([args.o])

    if not args.e:
        reload.oomox(args.g)
        reload.gtk()


def main():
    """Main script function."""
    util.setup_logging()
    args = get_args(sys.argv[1:])
    process_args(args)


if __name__ == "__main__":
    main()
