"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
from pywal import export
from pywal import image
from pywal import magic
from pywal import reload
from pywal import sequences
from pywal import wallpaper


def get_image(img):
    """Validate image input."""
    return image.get_image(img)


def create_palette(img, quiet=False):
    """Create a palette and return it as a dict."""
    return magic.get_colors(img, quiet)


def send_sequences(colors, vte):
    """Send the sequences."""
    sequences.send_sequences(colors, vte)


def reload_env():
    """Reload the environment."""
    reload.reload_env()


def export_all_templates(colors, template_dir=None, export_dir=None):
    """Export all templates."""
    export.export_all_templates(colors, template_dir, export_dir)


def set_wallpaper(img):
    """Set the wallpaper."""
    wallpaper.set_wallpaper(img)


def reload_colors(vte, sequence_file=None):
    """Reload the colors."""
    sequences.reload_colors(vte, sequence_file)
