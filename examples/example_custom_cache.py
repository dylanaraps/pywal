"""Test script for wal api.
   This script uses a custom cache location for the files."""
import pathlib
import pywal


CACHE_DIR = pathlib.Path.home() / "wal-test"
COLOR_COUNT = 16


def main():
    """Main function."""
    # Create the custom cache directory.
    pywal.util.create_dir(CACHE_DIR / "schemes")

    # Validate image and pick a random image if a
    # directory is given below.
    #
    # CACHE_DIR is an optional argument and is used to check the current
    # wallpaper against the random selection. This prevents shuffling to
    # the identical image when a directory is passed as an argument.
    image = pywal.get_image("/home/dylan/Pictures/Wallpapers/", CACHE_DIR)

    # Return a dict with the palette.
    #
    # The last argument is 'quiet' mode. When set to true, no notifications
    # are displayed.
    colors = pywal.create_palette(image, CACHE_DIR, COLOR_COUNT, True)

    # Apply the palette to all open terminals.
    # Second argument is a boolean for VTE terminals.
    # Set it to true if the terminal you're using is
    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
    pywal.send_sequences(colors, False, CACHE_DIR)

    # Reload xrdb, i3 and polybar.
    pywal.reload_env(CACHE_DIR)

    # Export template files.
    pywal.export_all_templates(colors, CACHE_DIR)

    # Set the wallpaper.
    pywal.set_wallpaper(image)


main()
