"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
import pathlib

from pywal import image
from pywal import magic
from pywal import reload
from pywal import sequences
from pywal import template
from pywal import wallpaper


__version__ = "0.4.0"


COLOR_COUNT = 16
CACHE_DIR = pathlib.Path.home() / ".cache/wal/"


def get_image(img, cache_dir=CACHE_DIR):
    """Validate image input."""
    return image.get_image(img, cache_dir)


def create_palette(img, cache_dir=CACHE_DIR,
                   color_count=COLOR_COUNT, quiet=True):
    """Create a palette and return it as a dict."""
    return magic.get_colors(img, cache_dir, color_count, quiet)


def send_sequences(colors, vte, cache_dir=CACHE_DIR):
    """Send the sequences."""
    sequences.send_sequences(colors, vte, cache_dir)


def reload_env(cache_dir=CACHE_DIR):
    """Reload the environment."""
    reload.reload_env(cache_dir)


def export_all_templates(colors, output_dir=CACHE_DIR, template_dir=None):
    """Export all templates."""
    template.export_all_templates(colors, output_dir, template_dir)


def set_wallpaper(img):
    """Set the wallpaper."""
    wallpaper.set_wallpaper(img)


def reload_colors(vte, cache_dir=CACHE_DIR):
    """Reload the colors."""
    sequences.reload_colors(vte, cache_dir)
