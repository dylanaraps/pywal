"""Set the wallpaper."""
import os
import shutil
import subprocess
import dbus # I didn't manage to do this on the command line using qdbus

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
    
    desktop = os.environ.get("KDE_SESSION_UID") # I think
    if desktop:
        return "KDE"

def xfconf(path, img):
    """Call xfconf to set the wallpaper on XFCE."""
    util.disown("xfconf-query", "--channel", "xfce4-desktop",
                "--property", path, "--set", img)


def set_wm_wallpaper(img):
    """Set the wallpaper for non desktop environments."""
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
                          "picture-uri", "file://" + img])

    elif "gnome" in desktop:
        subprocess.Popen(["gsettings", "set",
                          "org.gnome.desktop.background",
                          "picture-uri", "file://" + img])

    elif "mate" in desktop:
        subprocess.Popen(["gsettings", "set", "org.mate.background",
                          "picture-filename", img])
        
    elif "kde" in desktop:
        jscript = """
        var allDesktops = desktops();
        print (allDesktops);
        for (i=0;i<allDesktops.length;i++) {
            d = allDesktops[i];
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
            d.writeConfig("Image", "file://%s")
        }
        """
        # Using the modulo operator is faster than using str.format
        bus = dbus.SessionBus()
        plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
        plasma.evaluateScript(jscript % img)       

    else:
        set_wm_wallpaper(img)


def set_wallpaper(img):
    """Set the wallpaper."""
    if not os.path.isfile(img):
        return

    desktop = get_desktop_env()

    if desktop:
        set_desktop_wallpaper(desktop, img)

    else:
        set_wm_wallpaper(img)

    print("wallpaper: Set the new wallpaper")
