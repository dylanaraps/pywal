"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps.
"""
from pywal import image
from pywal import magic
from pywal import reload
from pywal import sequences
from pywal import wallpaper


def get_image(img):
    """Validate image input."""
    return image.get_image(img)


def create_palette(img):
    """Create a palette and return it as a dict."""
    colors = magic.gen_colors(img)
    colors = magic.sort_colors(img, colors)
    return colors


def send_sequences(colors, vte):
    """Send the sequences."""
    sequences.send_sequences(colors, vte)


def reload_env():
    """Reload the environment."""
    reload.reload_env()


def set_wallpaper(img):
    """Set the wallpaper."""
    wallpaper.set_wallpaper(img)


# def reload_colors(vte):
#     """Reload the colors."""
#     sequences.reload_colors(vte)
