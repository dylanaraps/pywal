"""
Misc helper functions.
"""
import os
import pathlib
import subprocess
import shutil

from pywal import settings as s


def read_file(input_file):
    """Read colors from a file."""
    return open(input_file).read().splitlines()


def save_file(colors, export_file):
    """Write the colors to the file."""
    with open(export_file, "w") as file:
        file.write(colors)


def create_cache_dir():
    """Alias to create the cache dir."""
    pathlib.Path(s.CACHE_DIR / "schemes").mkdir(parents=True, exist_ok=True)


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    red, green, blue = list(bytes.fromhex(color.strip("#")))
    return f"{red},{green},{blue}"


def fix_escape(string):
    """Decode a string."""
    return bytes(string, "utf-8").decode("unicode_escape")


def notify(msg):
    """Send arguements to notify-send."""
    if shutil.which("notify-send") and s.Args.notify:
        subprocess.Popen(["notify-send", msg],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         preexec_fn=os.setpgrp)


def disown(*cmd):
    """Call a system command in the background,
       disown it and hide it's output."""
    subprocess.Popen(["nohup"] + list(cmd),
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     preexec_fn=os.setpgrp)
