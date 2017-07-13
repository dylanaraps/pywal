"""
Global Constants.
"""
import pathlib
import platform


__version__ = "0.4.0"


COLOR_COUNT = 16
CACHE_DIR = pathlib.Path.home() / ".cache/wal/"
OS = platform.uname()[0]
