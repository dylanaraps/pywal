"""
Setup and handling of pywal config file.
"""
from . import util
from .settings import DEFAULT_CONF_FILE, CONF_FILE


def load():
    """Setup config file."""
    util.copy_file_if(DEFAULT_CONF_FILE, CONF_FILE)

    config = {}
    exec(open(CONF_FILE).read(), config)

    return config
