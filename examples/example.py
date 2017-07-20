"""pywal api example."""
import pywal


def main():
    """Main function."""
    image = "/home/dylan/Pictures/Wallpapers/anVmEaA.jpg"

    # Return a dict with the palette.
    colors = pywal.create_palette(image)

    # Apply the palette to all open terminals.
    # Second argument is a boolean for VTE terminals.
    # Set it to true if the terminal you're using is
    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
    pywal.send_sequences(colors, False)

    # Reload xrdb, i3 and polybar.
    pywal.reload_env()

    # Set the wallpaper.
    pywal.set_wallpaper(image)


main()
