"""
Global Constants.
"""
import os
import pathlib


__version__ = "0.2.6"


# Internal variables.
COLOR_COUNT = 16
CACHE_DIR = pathlib.Path.home() / ".cache/wal/"
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
