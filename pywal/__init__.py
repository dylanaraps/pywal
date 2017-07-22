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

from .settings import __version__
from .colors import get as create_palette
from .image import get as get_image
from .reload import colors as reload_colors
from .reload import env as reload_env
from .sequences import send as send_sequences
from .template import export_all as export_all_templates
from .wallpaper import change as set_wallpaper

__all__ = [
    "__version__",
    "create_palette",
    "export_all_templates",
    "get_image",
    "reload_colors",
    "reload_env",
    "send_sequences",
    "set_wallpaper",
]
