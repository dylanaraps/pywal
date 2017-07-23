"""
Reload programs.
"""
import re
import shutil
import subprocess

from .settings import __cache_dir__
from . import util


def xrdb(xrdb_file=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_file = xrdb_file or __cache_dir__ / "colors.Xresources"

    if shutil.which("xrdb"):
        subprocess.call(["xrdb", "-merge", xrdb_file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


def i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown("i3-msg", "reload")


def polybar():
    """Reload polybar colors."""
    if shutil.which("polybar"):
        util.disown("pkill", "-USR1", "polybar")


def env(xrdb_file=None):
    """Reload environment."""
    xrdb(xrdb_file)
    i3()
    polybar()
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
