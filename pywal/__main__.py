"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
import argparse
import os
import shutil
import sys

from pywal.settings import CACHE_DIR, __version__
from pywal import export
from pywal import image
from pywal import magic
from pywal import reload
from pywal import sequences
from pywal import util
from pywal import wallpaper


def get_args():
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

    # Add the args.
    arg.add_argument("-c", action="store_true",
                     help="Delete all cached colorschemes.")

    arg.add_argument("-i", metavar="\"/path/to/img.jpg\"",
                     help="Which image or directory to use.")

    arg.add_argument("-f", metavar="\"/path/to/colorscheme/file\"",
                     help="Which colorscheme file to use.")

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

    if args.i and args.f:
        print("error: Conflicting arguments -i and -f.\n"
              "       Refer to \"wal -h\" for more info.")
        exit(1)

    # -q
    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, "w")

    # -c
    if args.c:
        shutil.rmtree(CACHE_DIR / "schemes")
        util.create_dir(CACHE_DIR / "schemes")

    # -r
    if args.r:
        sequences.reload_colors(args.t)

    # -v
    if args.v:
        print(f"wal {__version__}")
        exit(0)

    # -i
    if args.i:
        image_file = image.get_image(args.i)
        colors_plain = magic.get_colors(image_file, args.q)

    # -f
    elif args.f:
        colors_plain = util.read_file_json(args.f)

    # -i or -f
    if args.i or args.f:
        sequences.send_sequences(colors_plain, args.t)

        if not args.n:
            wallpaper.set_wallpaper(colors_plain["wallpaper"])

        export.export_all_templates(colors_plain)
        reload.reload_env()

    # -o
    if args.o:
        util.disown(args.o)


def main():
    """Main script function."""
    util.create_dir(CACHE_DIR / "schemes")
    args = get_args()
    process_args(args)

    # This saves 10ms.
    # pylint: disable=W0212
    # os._exit(0)


if __name__ == "__main__":
    main()
