"""
Misc helper functions.
"""
import os
import pathlib
import subprocess


def read_file(input_file):
    """Read colors from a file."""
    with open(input_file) as file:
        colors = file.read().splitlines()
    return colors


def save_file(colors, export_file):
    """Write the colors to the file."""
    with open(export_file, "w") as file:
        file.write(colors)


def create_dir(directory):
    """Alias to create the cache dir."""
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    red, green, blue = list(bytes.fromhex(color.strip("#")))
    return f"{red},{green},{blue}"


def disown(*cmd):
    """Call a system command in the background,
       disown it and hide it's output."""
    subprocess.Popen(["nohup"] + list(cmd),
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     preexec_fn=os.setpgrp)
