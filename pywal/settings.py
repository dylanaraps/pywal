"""
                                      '||
... ...  .... ... ... ... ...  ....    ||
 ||'  ||  '|.  |   ||  ||  |  '' .||   ||
 ||    |   '|.|     ||| |||   .|' ||   ||
 ||...'     '|       |   |    '|..'|' .||.
 ||      .. |
''''      ''
Created by Dylan Araps.
"""

import pathlib
import platform


__version__ = "0.5.11"


HOME = pathlib.Path.home()
CACHE_DIR = HOME / ".cache/wal/"
MODULE_DIR = pathlib.Path(__file__).parent
COLOR_COUNT = 16
OS = platform.uname()[0]
