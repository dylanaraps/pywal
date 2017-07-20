"""
Misc helper functions.
"""
import json
import os
import pathlib
import subprocess


class Color:
    """Color formats."""
    def __init__(self, hex_color):
        self.hex_color = hex_color

    def __str__(self):
        return self.hex_color

    @property
    def rgb(self):
        """Convert a hex color to rgb."""
        return hex_to_rgb(self.hex_color)

    @property
    def xrgba(self):
        """Convert a hex color to xrdb rgba."""
        return hex_to_xrgba(self.hex_color)


def set_grey(colors):
    """Set a grey color based on the brightness
       of another color."""
    return {
        "0": "#666666",
        "1": "#666666",
        "2": "#757575",
        "3": "#999999",
        "4": "#999999",
        "5": "#8a8a8a",
        "6": "#a1a1a1",
        "7": "#a1a1a1",
        "8": "#a1a1a1",
        "9": "#a1a1a1",
    }.get(colors[0][1], colors[7])


def read_file(input_file):
    """Read data from a file."""
    with open(input_file) as file:
        data = file.read().splitlines()
    return data


def read_file_json(input_file):
    """Read data from a json file."""
    with open(input_file) as json_file:
        data = json.load(json_file)

    # If wallpaper is unset, set it to "None"
    if "wallpaper" not in data:
        data["wallpaper"] = "None"

    return data


def save_file(data, export_file):
    """Write data to a file."""
    with open(export_file, "w") as file:
        file.write(data)


def save_file_json(data, export_file):
    """Write data to a json file."""
    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)


def create_dir(directory):
    """Alias to create the cache dir."""
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    red, green, blue = list(bytes.fromhex(color.strip("#")))
    return f"{red},{green},{blue}"


def hex_to_xrgba(color):
    """Convert a hex color to xrdb rgba."""
    col = color.lower()
    return f"{col[1]}{col[2]}/{col[3]}{col[4]}/{col[5]}{col[6]}/ff"


def disown(*cmd):
    """Call a system command in the background,
       disown it and hide it's output."""
    subprocess.Popen(["nohup"] + list(cmd),
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     preexec_fn=os.setpgrp)
