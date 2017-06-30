"""
Get the image file.
"""
import os
import pathlib
import random

from pywal.settings import CACHE_DIR
from pywal import util


def get_random_image(img_dir):
    """Pick a random image file from a directory."""
    current_wall = CACHE_DIR / "wal"

    if current_wall.is_file():
        current_wall = util.read_file(current_wall)
        current_wall = os.path.basename(current_wall[0])

    # Add all images to a list excluding the current wallpaper.
    file_types = (".png", ".jpg", ".jpeg", ".jpe", ".gif")
    images = [img for img in os.scandir(img_dir)
              if img.name.endswith(file_types) and img.name != current_wall]

    # If no images are found, use the current wallpaper.
    if not images:
        print("image: No new images found (nothing to do), exiting...")
        quit(1)

    return img_dir / random.choice(images).name


def get_image(img):
    """Validate image input."""
    image = pathlib.Path(img)

    if image.is_file():
        wal_img = image

    elif image.is_dir():
        wal_img = get_random_image(image)

    else:
        print("error: No valid image file found.")
        exit(1)

    print("image: Using image", wal_img)
    return str(wal_img)
