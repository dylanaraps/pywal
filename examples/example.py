"""Simple script for wal api."""
import pywal


def main():
    """Main function."""
    # Validate image and pick a random image if a
    # directory is given below.
    image = pywal.get_image("/home/dylan/Pictures/Wallpapers/")

    # Return a dict with the palette.
    # Set quiet to 'True' to disable notifications.
    colors = pywal.create_palette(image, quiet=False)

    # Apply the palette to all open terminals.
    # Second argument is a boolean for VTE terminals.
    # Set it to true if the terminal you're using is
    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
    pywal.send_sequences(colors, vte=False)

    # Reload xrdb, i3 and polybar.
    pywal.reload_env()

    # Export template files.
    pywal.export_all_templates(colors)

    # Set the wallpaper.
    pywal.set_wallpaper(image)


main()
