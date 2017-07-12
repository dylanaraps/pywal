"""
Reload programs.
"""
import shutil
import subprocess

from pywal.settings import CACHE_DIR
from pywal import util


def reload_xrdb():
    """Merge the colors into the X db so new terminals use them."""
    if shutil.which("xrdb"):
        subprocess.call(["xrdb", "-merge", CACHE_DIR / "colors.Xresources"])


def reload_i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown("i3-msg", "reload")


def reload_polybar():
    """Reload polybar colors."""
    if shutil.which("polybar"):
        util.disown("pkill", "-USR1", "polybar")


def reload_env():
    """Reload environment."""
    reload_xrdb()
    reload_i3()
    reload_polybar()
    print("reload: Reloaded environment.")
