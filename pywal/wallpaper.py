"""Set the wallpaper."""
import os
import shutil
import subprocess

from pywal import util


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
    util.disown("xfconf-query", "--channel", "xfce4-desktop",
                "--property", path, "--set", img)


def set_desktop_wallpaper(desktop, img):
    """Set the wallpaper for the desktop environment."""
    desktop = str(desktop).lower()

    if "xfce" in desktop or "xubuntu" in desktop:
        # XFCE requires two commands since they differ between versions.
        xfconf("/backdrop/screen0/monitor0/image-path", img)
        xfconf("/backdrop/screen0/monitor0/workspace0/last-image", img)

    elif "muffin" in desktop or "cinnamon" in desktop:
        subprocess.Popen(["gsettings", "set",
                          "org.cinnamon.desktop.background",
                          "picture-uri", "file:///" + img])

    elif "gnome" in desktop:
        subprocess.Popen(["gsettings", "set",
                          "org.gnome.desktop.background",
                          "picture-uri", "file:///" + img])

    elif "mate" in desktop:
        subprocess.Popen(["gsettings", "set", "org.mate.background",
                          "picture-filename", img])


def set_wallpaper(img):
    """Set the wallpaper."""
    desktop = get_desktop_env()

    if desktop:
        set_desktop_wallpaper(desktop, img)

    else:
        if shutil.which("feh"):
            subprocess.Popen(["feh", "--bg-fill", img])

        elif shutil.which("nitrogen"):
            subprocess.Popen(["nitrogen", "--set-zoom-fill", img])

        elif shutil.which("bgs"):
            subprocess.Popen(["bgs", img])

        elif shutil.which("hsetroot"):
            subprocess.Popen(["hsetroot", "-fill", img])

        elif shutil.which("habak"):
            subprocess.Popen(["habak", "-mS", img])

        else:
            print("error: No wallpaper setter found.")
            return

    print("wallpaper: Set the new wallpaper")
    return 0
