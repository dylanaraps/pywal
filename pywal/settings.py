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

import configparser
import os
import platform


__version__ = "1.3.3"
__cache_version__ = "1.0.0"

HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
CACHE_DIR = os.path.join(HOME, ".cache", "wal")
MODULE_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.join(HOME, ".config", "wal")
OS = platform.uname()[0]

CONFIG = configparser.ConfigParser()
CONFIG.read("/home/black/.config/wal/config.ini")
