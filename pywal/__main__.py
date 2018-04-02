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
from . import config
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
                     const="list_backends", nargs="?", default="default")

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

    return arg


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.error("wal needs to be given arguments to run.")

    if args.v:
        parser.exit(0, "wal %s\n" % __version__)

    if args.i and args.theme:
        parser.error("Conflicting arguments -i and -f.")

    if not args.i and \
       not args.theme and \
       not args.R and \
       not args.backend:
        parser.error("No input specified.\n"
                     "--backend, --theme, -i or -R are required.")

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


def parse_args(parser, conf):
    """Process args."""
    args = parser.parse_args()

    if args.a:
        conf["alpha"] = args.a

    if args.backend:
        conf["backend"] = args.backend

    if args.b:
        conf["background"] = "#%s" % (args.b.strip("#"))

    if args.c:
        conf["cache"] = False

    if args.e:
        conf["reload"] = False

    if args.g:
        conf["oomox"] = True

    if args.i:
        conf["image"] = args.i

    if args.theme:
        conf["theme"] = args.theme

    if args.l:
        conf["type"] = "light" if args.l else "dark"

    if args.n:
        conf["wallpaper"] = False

    if args.o:
        conf["cmd_hook"] = args.o

    if args.q:
        conf["quiet"] = True

    if args.s:
        conf["sequences"] = False

    if args.t:
        conf["tty"] = False

    if args.R:
        conf["restore"] = True

    return conf


def wal(conf):
    """Start the show."""
    if conf.get("quiet", False):
        logging.getLogger().disabled = True
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if not conf.get("cache", True):
        scheme_dir = os.path.join(CACHE_DIR, "schemes")
        shutil.rmtree(scheme_dir, ignore_errors=True)

    if conf.get("image"):
        image_file = image.get(conf.get("image"))
        cols = colors.get(image_file, conf.get("type"), conf.get("backend"))

    if conf.get("theme"):
        cols = theme.file(conf.get("theme"))

    if conf.get("restore"):
        cols = theme.file(os.path.join(CACHE_DIR, "colors.json"))

    if conf.get("alpha"):
        util.Color.alpha_num = conf.get("alpha", "100")

    if conf.get("background"):
        cols["special"]["background"] = conf.get("background")
        cols["colors"]["color0"] = conf.get("background")

    if conf.get("wallpaper"):
        wallpaper.change(cols["wallpaper"])

    sequences.send(cols, to_send=conf.get("sequences"))

    if sys.stdout.isatty():
        colors.palette()

    export.every(cols)

    if conf.get("reload"):
        reload.env(tty_reload=conf.get("tty"))

    if conf.get("cmd_hook"):
        util.disown(conf.get("cmd_hook"))

    if conf.get("reload"):
        reload.oomox(conf.get("oomox"))
        reload.gtk()


def main():
    """Main script function."""
    util.setup_logging()

    parser = get_args()
    parse_args_exit(parser)

    conf = config.load()
    conf = parse_args(parser, conf)

    wal(conf)


if __name__ == "__main__":
    main()
