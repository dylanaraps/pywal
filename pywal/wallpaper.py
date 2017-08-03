"""Set the wallpaper."""
import os
import shutil
import subprocess

from .settings import CACHE_DIR, HOME, OS
from . import util


def get_desktop_env():
    """Identify the current running desktop environment."""
    desktop = os.environ.get("XDG_CURRENT_DESKTOP")
    if desktop:
        return desktop

    desktop = os.environ.get("DESKTOP_SESSION")
    if desktop:
        return desktop

    desktop = os.environ.get("GNOME_DESKTOP_SESSION_ID")
    if desktop:
        return "GNOME"

    desktop = os.environ.get("MATE_DESKTOP_SESSION_ID")
    if desktop:
        return "MATE"


def xfconf(path, img):
    """Call xfconf to set the wallpaper on XFCE."""
    util.disown(["xfconf-query", "--channel", "xfce4-desktop",
                 "--property", path, "--set", img])


def set_wm_wallpaper(img):
    """Set the wallpaper for non desktop environments."""
    if shutil.which("feh"):
        util.disown(["feh", "--bg-fill", img])

    elif shutil.which("nitrogen"):
        util.disown(["nitrogen", "--set-zoom-fill", img])

    elif shutil.which("bgs"):
        util.disown(["bgs", img])

    elif shutil.which("hsetroot"):
        util.disown(["hsetroot", "-fill", img])

    elif shutil.which("habak"):
        util.disown(["habak", "-mS", img])

    else:
        print("error: No wallpaper setter found.")
        return


def set_desktop_wallpaper(desktop, img):
    """Set the wallpaper for the desktop environment."""
    desktop = str(desktop).lower()

    if "xfce" in desktop or "xubuntu" in desktop:
        # XFCE requires two commands since they differ between versions.
        xfconf("/backdrop/screen0/monitor0/image-path", img)
        xfconf("/backdrop/screen0/monitor0/workspace0/last-image", img)

    elif "muffin" in desktop or "cinnamon" in desktop:
        util.disown(["gsettings", "set",
                     "org.cinnamon.desktop.background",
                     "picture-uri", "file://" + img])

    elif "gnome" in desktop:
        util.disown(["gsettings", "set",
                     "org.gnome.desktop.background",
                     "picture-uri", "file://" + img])

    elif "mate" in desktop:
        util.disown(["gsettings", "set", "org.mate.background",
                     "picture-filename", img])

    else:
        set_wm_wallpaper(img)


def set_mac_wallpaper(img):
    """Set the wallpaper on macOS."""
    db_file = HOME / "Library/Application Support/Dock/desktoppicture.db"
    subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])

    # Kill the dock to fix issues with cached wallpapers.
    # macOS caches wallpapers and if a wallpaper is set that shares
    # the filename with a cached wallpaper, the cached wallpaper is
    # used instead.
    subprocess.call(["killall", "Dock"])


def change(img):
    """Set the wallpaper."""
    if not os.path.isfile(img):
        return

    desktop = get_desktop_env()

    if OS == "Darwin":
        set_mac_wallpaper(img)

    elif desktop:
        set_desktop_wallpaper(desktop, img)

    else:
        set_wm_wallpaper(img)

    print("wallpaper: Set the new wallpaper.")


def get(cache_dir=CACHE_DIR):
    """Get the current wallpaper."""
    current_wall = cache_dir / "wal"

    if current_wall.is_file():
        return util.read_file(current_wall)[0]

    return "None"
