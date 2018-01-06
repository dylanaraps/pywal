"""
Reload programs.
"""
import os
import shutil
import subprocess
import sys

from .settings import CACHE_DIR, HOME, MODULE_DIR, OS
from . import util


def tty():
    """Load colors in tty."""
    tty_script = os.path.join(CACHE_DIR, "colors-tty.sh")

    if os.path.isfile(tty_script):
        subprocess.Popen(["sh", tty_script])


def xrdb(xrdb_files=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_files = xrdb_files or \
        [os.path.join(CACHE_DIR, "colors.Xresources"),
         os.path.join(CACHE_DIR, "colors-rofi.Xresources")]

    if shutil.which("xrdb") and OS != "Darwin":
        for file in xrdb_files:
            subprocess.run(["xrdb", "-merge", "-nocpp", file])


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


def sway():
    """Reload sway colors."""
    if shutil.which("swaymsg"):
        util.disown(["swaymsg", "reload"])


def colors(cache_dir=CACHE_DIR):
    """Reload colors. (Deprecated)"""
    sequences = os.path.join(cache_dir, "sequences")

    sys.stderr.write("'wal -r' is deprecated: "
                     "Use 'cat %s' instead.\n" % sequences)

    if os.path.isfile(sequences):
        print("".join(util.read_file(sequences)), end="")


def env(xrdb_file=None):
    """Reload environment."""
    gtk()
    xrdb(xrdb_file)
    i3()
    sway()
    polybar()
    print("reload: Reloaded environment.")
    tty()
