"""
Reload programs.
"""
import os
import re
import shutil
import subprocess
import sys

from .settings import CACHE_DIR, HOME, MODULE_DIR, OS
from . import util


def xrdb(xrdb_file=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_file = xrdb_file or os.path.join(CACHE_DIR, "colors.Xresources")

    if shutil.which("xrdb") or OS != "Darwin":
        subprocess.Popen(["xrdb", "-merge", xrdb_file],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL).wait()


def gtk():
    """Move gtkrc files to the correct location."""
    theme_path = os.path.join(HOME, ".themes", "Flatabulous-wal")
    gtk2_file = os.path.join(CACHE_DIR, "colors-gtk2.rc")

    if os.path.isdir(theme_path):
        shutil.copy(gtk2_file, os.path.join(theme_path, "gtk-2.0"))

    # Here we call a Python 2 script to reload the GTK themes.
    # This is done because the Python 3 GTK/Gdk libraries don't
    # provide a way of doing this.
    if shutil.which("python2"):
        gtk_reload = os.path.join(MODULE_DIR, "scripts", "gtk_reload.py")
        util.disown(["python2", gtk_reload])

    else:
        print("warning: GTK2 reload support requires Python 2.")


def i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown(["i3-msg", "reload"])


def polybar():
    """Reload polybar colors."""
    if shutil.which("polybar"):
        util.disown(["pkill", "-USR1", "polybar"])


def env(xrdb_file=None):
    """Reload environment."""
    gtk()
    xrdb(xrdb_file)
    i3()
    polybar()
    print("reload: Reloaded environment.")


def colors(vte, cache_dir=CACHE_DIR):
    """Reload the current scheme."""
    sequence_file = os.path.join(cache_dir, "sequences")

    if os.path.isfile(sequence_file):
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the unsupported sequence.
        if vte:
            sequences = re.sub(r"\]708;(\[.{0,3}\])?\#.{6}", "", sequences)

        print(sequences, end="")

    sys.exit(0)
