"""
Reload programs.
"""
import re
import shutil
import subprocess

from .settings import __cache_dir__
from . import util


def reload_xrdb(cache_dir):
    """Merge the colors into the X db so new terminals use them."""
    if shutil.which("xrdb"):
        subprocess.call(["xrdb", "-merge", cache_dir / "colors.Xresources"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


def reload_i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown("i3-msg", "reload")


def reload_polybar():
    """Reload polybar colors."""
    if shutil.which("polybar"):
        util.disown("pkill", "-USR1", "polybar")


def env(cache_dir=__cache_dir__):
    """Reload environment."""
    reload_xrdb(cache_dir)
    reload_i3()
    reload_polybar()
    print("reload: Reloaded environment.")


def colors(vte, cache_dir=__cache_dir__):
    """Reload the current scheme."""
    sequence_file = cache_dir / "sequences"

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the unsupported sequence.
        if vte:
            sequences = re.sub(r"\]708;\#.{6}", "", sequences)

        print(sequences, end="")

    exit(0)
