"""
Get the image file.
"""
import logging
import os
import random
import re
import sys

from .settings import CACHE_DIR
from . import util
from . import wallpaper


def get_image_dir_recursive(img_dir):
    """Get all images in a directory recursively."""
    current_wall = wallpaper.get()
    current_wall = os.path.basename(current_wall)

    file_types = (".png", ".jpg", ".jpeg", ".jpe", ".gif")

    images = []
    for path, _, files in os.walk(img_dir):
        for name in files:
            if name.lower().endswith(file_types):
                if name.endswith(current_wall):
                    current_wall = os.path.join(path, name)
                images.append(os.path.join(path, name))

    return images, current_wall


def get_image_dir(img_dir):
    """Get all images in a directory."""
    current_wall = wallpaper.get()
    current_wall = os.path.basename(current_wall)

    file_types = (".png", ".jpg", ".jpeg", ".jpe", ".gif")

    return [img.name for img in os.scandir(img_dir)
            if img.name.lower().endswith(file_types)], current_wall


def get_random_image(img_dir, recursive):
    """Pick a random image file from a directory."""
    if recursive:
        images, current_wall = get_image_dir_recursive(img_dir)
    else:
        images, current_wall = get_image_dir(img_dir)

    if len(images) > 2 and current_wall in images:
        images.remove(current_wall)

    elif not images:
        logging.error("No images found in directory.")
        sys.exit(1)

    random.shuffle(images)
    return os.path.join(img_dir if not recursive else "", images[0])


def get_next_image(img_dir, recursive):
    """Get the next image in a dir."""
    if recursive:
        images, current_wall = get_image_dir_recursive(img_dir)
    else:
        images, current_wall = get_image_dir(img_dir)

    images.sort(key=lambda img: [int(x) if x.isdigit() else x
                                 for x in re.split('([0-9]+)', img)])

    try:
        next_index = images.index(current_wall) + 1

    except ValueError:
        next_index = 0

    try:
        image = images[next_index]

    except IndexError:
        image = images[0]

    return os.path.join(img_dir if not recursive else "", image)


def get(img, cache_dir=CACHE_DIR, iterative=False, recursive=False):
    """Validate image input."""
    if os.path.isfile(img):
        wal_img = img

    elif os.path.isdir(img):
        if iterative:
            wal_img = get_next_image(img, recursive)

        else:
            wal_img = get_random_image(img, recursive)

    else:
        logging.error("No valid image file found.")
        sys.exit(1)

    wal_img = os.path.abspath(wal_img)

    # Cache the image file path.
    util.save_file(wal_img, os.path.join(cache_dir, "wal"))

    logging.info("Using image \033[1;37m%s\033[0m.", os.path.basename(wal_img))
    return wal_img
