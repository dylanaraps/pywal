"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
from pywal.wal import __version__
from pywal.wal import create_palette
from pywal.wal import export_all_templates
from pywal.wal import get_image
from pywal.wal import reload_colors
from pywal.wal import reload_env
from pywal.wal import send_sequences
from pywal.wal import set_wallpaper

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
