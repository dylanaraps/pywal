"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
import argparse
import os
import shutil
import sys

from pywal import settings as s
from pywal import export
from pywal import gen_colors
from pywal import set_colors
from pywal import wallpaper
from pywal import util


__version__ = "0.1.6"


def get_args():
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

    # Add the args.
    arg.add_argument("-c", action="store_true",
                     help="Delete all cached colorschemes.")

    arg.add_argument("-i", metavar="\"/path/to/img.jpg\"",
                     help="Which image or directory to use.")

    arg.add_argument("-n", action="store_true",
                     help="Skip setting the wallpaper.")

    arg.add_argument("-o", metavar="\"script_name\"",
                     help="External script to run after \"wal\".")

    arg.add_argument("-q", action="store_true",
                     help="Quiet mode, don\"t print anything and \
                           don't display notifications.")

    arg.add_argument("-r", action="store_true",
                     help="Reload current colorscheme.")

    arg.add_argument("-t", action="store_true",
                     help="Fix artifacts in VTE Terminals. \
                           (Termite, xfce4-terminal)")

    arg.add_argument("-v", action="store_true",
                     help="Print \"wal\" version.")

    return arg.parse_args()


def process_args(args):
    """Process args."""
    # If no args were passed.
    if not len(sys.argv) > 1:
        print("error: wal needs to be given arguments to run.\n"
              "       Refer to \"wal -h\" for more info.")
        exit(1)

    # -q
    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, "w")
        s.Args.notify = False

    # -c
    if args.c:
        shutil.rmtree(s.CACHE_DIR / "schemes")
        util.create_cache_dir()

    # -r
    if args.r:
        gen_colors.reload_colors(args.t)

    # -v
    if args.v:
        print(f"wal {__version__}")
        exit(0)

    # -i
    if args.i:
        image = gen_colors.get_image(args.i)
        s.ColorType.plain = gen_colors.get_colors(image)

        if not args.n:
            wallpaper.set_wallpaper(image)

        # Set the colors.
        set_colors.send_sequences(s.ColorType.plain, args.t)
        export.export_colors(s.ColorType.plain)

    # -o
    if args.o:
        util.disown(args.o)


def main():
    """Main script function."""
    util.create_cache_dir()
    args = get_args()
    process_args(args)

    # This saves 10ms.
    # pylint: disable=W0212
    # os._exit(0)


if __name__ == "__main__":
    main()
