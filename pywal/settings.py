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
import shutil

from . import util


__version__ = "1.3.3"
__cache_version__ = "1.0.0"


HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
CACHE_DIR = os.path.join(HOME, ".cache", "wal")
MODULE_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.join(HOME, ".config", "wal")
CONF_FILE = os.path.join(CONF_DIR, "config.ini")
DEFAULT_CONF_FILE = os.path.join(MODULE_DIR, "config", "config.ini")
OS = platform.uname()[0]


if not os.path.isfile(CONF_FILE):
    util.create_dir(CONF_DIR)
    shutil.copy2(DEFAULT_CONF_FILE, CONF_DIR)


CONFIG = configparser.ConfigParser()
CONFIG.read(CONF_FILE)
