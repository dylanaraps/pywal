"""
Global variables and classes.
"""
import pathlib


__version__ = "0.2.0"


# Internal variables.
COLOR_COUNT = 16
CACHE_DIR = pathlib.Path.home() / ".cache/wal/"


# pylint: disable=too-few-public-methods
class Args(object):
    """Store args."""
    notify = True
