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


__version__ = "0.5.2"


HOME = pathlib.Path.home()
CACHE_DIR = HOME / ".cache/wal/"
MODULE_DIR = pathlib.Path(__file__).parent
COLOR_COUNT = 16
