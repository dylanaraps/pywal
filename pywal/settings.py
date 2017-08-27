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

import os
import platform


__version__ = "0.6.9"


HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
CACHE_DIR = os.path.join(HOME, ".cache", "wal")
MODULE_DIR = os.path.dirname(__file__)
COLOR_COUNT = 16
OS = platform.uname()[0]
