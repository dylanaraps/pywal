"""
Reload programs.
"""
import shutil
import subprocess

from pywal import util


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


def reload_env(cache_dir):
    """Reload environment."""
    reload_xrdb(cache_dir)
    reload_i3()
    reload_polybar()
    print("reload: Reloaded environment.")
