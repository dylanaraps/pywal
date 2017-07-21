"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
import argparse
import os
import shutil
import sys

from pywal import wal
from pywal import util


def get_args():
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

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
    if not len(sys.argv) > 1:
        print("error: wal needs to be given arguments to run.\n"
              "       Refer to \"wal -h\" for more info.")
        exit(1)

    if args.i and args.f:
        print("error: Conflicting arguments -i and -f.\n"
              "       Refer to \"wal -h\" for more info.")
        exit(1)

    if args.q:
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if args.c:
        shutil.rmtree(wal.CACHE_DIR / "schemes")
        util.create_dir(wal.CACHE_DIR / "schemes")

    if args.r:
        wal.reload_colors(args.t)

    if args.v:
        print(f"wal {wal.__version__}")
        exit(0)

    if args.i:
        image_file = wal.get_image(args.i)
        colors_plain = wal.create_palette(img=image_file, quiet=args.q)

    elif args.f:
        colors_plain = util.read_file_json(args.f)

    if args.i or args.f:
        wal.send_sequences(colors_plain, args.t)

        if not args.n:
            wal.set_wallpaper(colors_plain["wallpaper"])

        wal.export_all_templates(colors_plain)
        wal.reload_env()

    if args.o:
        util.disown(args.o)


def main():
    """Main script function."""
    util.create_dir(wal.CACHE_DIR / "schemes")
    args = get_args()
    process_args(args)

    # This saves 10ms.
    # pylint: disable=W0212
    # os._exit(0)


if __name__ == "__main__":
    main()
