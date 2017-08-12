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


__version__ = "0.6.0"


HOME = os.environ["HOME"]
CACHE_DIR = os.path.join(HOME, ".cache/wal/")
MODULE_DIR = os.path.dirname(__file__)
COLOR_COUNT = 16
OS = platform.uname()[0]
