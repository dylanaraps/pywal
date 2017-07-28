"""
Get the image file.
"""
import os
import pathlib
import random
import sys

from .settings import CACHE_DIR
from . import util
from . import wallpaper


def get_random_image(img_dir):
    """Pick a random image file from a directory."""
    current_wall = wallpaper.get()
    current_wall = os.path.basename(current_wall)

    file_types = (".png", ".jpg", ".jpeg", ".jpe", ".gif")
    images = [img for img in os.scandir(img_dir)
              if img.name.endswith(file_types) and img.name != current_wall]

    if not images:
        print("image: No new images found (nothing to do), exiting...")
        sys.exit(1)

    return str(img_dir / random.choice(images).name)


def get(img, cache_dir=CACHE_DIR):
    """Validate image input."""
    image = pathlib.Path(img)

    if image.is_file():
        wal_img = str(image)

    elif image.is_dir():
        wal_img = get_random_image(image)

    else:
        print("error: No valid image file found.")
        sys.exit(1)

    # Cache the image file path.
    util.save_file(wal_img, cache_dir / "wal")

    print("image: Using image", wal_img)
    return wal_img
