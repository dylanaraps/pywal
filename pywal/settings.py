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


__version__ = "3.3.0"
__cache_version__ = "1.1.0"


HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
CACHE_DIR = os.getenv("PYWAL_CACHE_DIR", os.path.join(HOME, ".cache", "wal"))
MODULE_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.join(HOME, ".config", "wal")
OS = platform.uname()[0]
