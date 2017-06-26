"""
Global variables and classes.
"""
import pathlib


__version__ = "0.2.0"


# Internal variables.
COLOR_COUNT = 16
CACHE_DIR = pathlib.Path.home() / ".cache/wal/"


# pylint: disable=too-few-public-methods
class ColorType(object):
    """Store colors in various formats."""
    plain = []
    xrdb = []
    sequences = []
    shell = []
    scss = []
    css = [":root {"]
    putty = [
        "Windows Registry Editor Version 5.00",
        "[HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\Sessions\\Wal]",
    ]


# pylint: disable=too-few-public-methods
class Args(object):
    """Store args."""
    notify = True
