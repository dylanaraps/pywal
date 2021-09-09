"""
Reload programs.
"""
import logging
import os
import shutil
import subprocess

from .settings import CACHE_DIR, XDG_CONF_DIR, MODULE_DIR, OS
from . import util


def tty(tty_reload):
    """Load colors in tty."""
    tty_script = os.path.join(CACHE_DIR, "colors-tty.sh")
    term = os.environ.get("TERM")

    if tty_reload and term == "linux":
        subprocess.Popen(["sh", tty_script])


def xrdb(xrdb_files=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_files = xrdb_files or \
        [os.path.join(CACHE_DIR, "colors.Xresources")]

    if shutil.which("xrdb") and OS != "Darwin":
        for file in xrdb_files:
            subprocess.run(["xrdb", "-merge", "-quiet", file], check=False)


def gtk():
    """Reload GTK2 theme on the fly."""
    # Here we call a Python 2 script to reload the GTK themes.
    # This is done because the Python 3 GTK/Gdk libraries don't
    # provide a way of doing this.
    if shutil.which("python2"):
        gtk_reload = os.path.join(MODULE_DIR, "scripts", "gtk_reload.py")
        util.disown(["python2", gtk_reload])

    else:
        logging.warning("GTK2 reload support requires Python 2.")
        
def gtk3():
    """Reload GTK3 theme on the fly, requires a theme that enables styling via gtk.css"""
    settings_ini = os.path.join(XDG_CONF_DIR, "gtk-3.0", "settings.ini")

    # Multiple backends available to set, xfsettings for xfce,
    # then gsd-settings in gnome, gsettings for everything else
    refresh_gsettings = (
        "gsettings set org.gnome.desktop.interface "
        "gtk-theme '' && sleep 0.1 && gsettings set "
        "org.gnome.desktop.interface gtk-theme '{}'"
    )

    refresh_xfsettings = (
        "xfconf-query -c xsettings -p /Net/ThemeName -s"
        " '' && sleep 0.1 && xfconf-query -c xsettings -p"
        " /Net/ThemeName -s '{}'"
    )

    if shutil.which("gsettings"):
        cmd = ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"]
        gsettings_theme = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        ).communicate()[0].decode().strip("' \n")

    xfsettings_theme = None
    if shutil.which("xfconf-query"):
        cmd = ["xfconf-query", "-c", "xsettings", "-p", "/Net/ThemeName"]
        xfsettings_theme = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        ).communicate()[0].decode().strip("' \n")

    if util.get_pid("gsd-settings") and gsettings_theme:
        subprocess.Popen(refresh_gsettings.format(gsettings_theme), shell=True)
        logging.info("Reloaded %s theme via gsd-settings" % gsettings_theme)

    elif util.get_pid("xfsettingsd") and xfsettings_theme:
        subprocess.Popen(refresh_xfsettings, shell=True)
        logging.info("reloaded %s theme via xfsettingsd" % xfsettings_theme)

    # no settings daemon is running.
    # So GTK is getting theme info from gtkrc file
    # using xsettingd to set the same theme (parsing it from gtkrc)
    elif shutil.which("xsettingsd") and os.path.isfile(settings_ini):
        gtkrc = configparser.ConfigParser()
        gtkrc.read(settings_ini)

        if gtkrc["Settings"]:
            theme = gtkrc["Settings"].get("gtk-theme-name", "FlatColor")
            fd, path = tempfile.mkstemp()

            try:
                with os.fdopen(fd, "w+") as tmp:
                    tmp.write('Net/ThemeName "' + theme + '"\n')
                    tmp.close()
                    util.silent_call([
                        "timeout", "0.2s", "xsettingsd", "-c", path
                    ])
                logging.info(
                    "reloaded %s from settings.ini using xsettingsd"
                    % theme
                )
            finally:
                os.remove(path)

    # The system has no known settings daemon installed,
    # but dconf gtk-theme exists, just refreshing its theme
    # Because user might be using unknown settings daemon
    elif shutil.which("gsettings") and gsettings_theme:
        subprocess.Popen(refresh_gsettings.format(gsettings_theme), shell=True)
        logging.warning(
            "No settings daemon found, just refreshing %s theme from gsettings"
            % gsettings_theme
        )


def i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg") and util.get_pid("i3"):
        util.disown(["i3-msg", "reload"])


def bspwm():
    """Reload bspwm colors."""
    if shutil.which("bspc") and util.get_pid("bspwm"):
        util.disown(["bspc", "wm", "-r"])


def kitty():
    """ Reload kitty colors. """
    if (shutil.which("kitty")
            and util.get_pid("kitty")
            and os.getenv('TERM') == 'xterm-kitty'):
        subprocess.call([
            "kitty", "@", "set-colors", "--all",
            os.path.join(CACHE_DIR, "colors-kitty.conf")
        ])


def polybar():
    """Reload polybar colors."""
    if shutil.which("polybar") and util.get_pid("polybar"):
        util.disown(["pkill", "-USR1", "polybar"])


def sway():
    """Reload sway colors."""
    if shutil.which("swaymsg") and util.get_pid("sway"):
        util.disown(["swaymsg", "reload"])


def colors(cache_dir=CACHE_DIR):
    """Reload colors. (Deprecated)"""
    sequences = os.path.join(cache_dir, "sequences")

    logging.error("'wal -r' is deprecated: "
                  "Use 'cat %s' instead.", sequences)

    if os.path.isfile(sequences):
        print("".join(util.read_file(sequences)), end="")


def env(xrdb_file=None, tty_reload=True):
    """Reload environment."""
    xrdb(xrdb_file)
    i3()
    bspwm()
    kitty()
    sway()
    polybar()
    logging.info("Reloaded environment.")
    tty(tty_reload)
