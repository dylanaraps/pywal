"""
GTK Theme handling.
"""
import shutil

from pywal.settings import CACHE_DIR, HOME


def gtk_move():
    """Move gtkrc files to the correct location."""
    theme_path = HOME / ".themes" / "Flatabulous-wal"
    gtk2_file = CACHE_DIR / "colors-gtk2.rc"
    gtk3_file = CACHE_DIR / "colors-gtk3.css"

    if theme_path.is_dir():
        if gtk2_file.is_file():
            shutil.copy(gtk2_file, theme_path / "gtk-2.0")

        if gtk3_file.is_file():
            shutil.copy(gtk3_file, theme_path / "gtk-3.0")


def gtk_main():
    """Main function to handle GTK."""
    gtk_move()
