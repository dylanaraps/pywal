"""
Export colors in various formats.
"""
import shutil
import subprocess

from pywal.settings import CACHE_DIR
from pywal import util
from pywal import format_colors


def save_colors(colors, export_file, message):
    """Export colors to var format."""
    colors = "".join(colors)
    util.save_file(colors, CACHE_DIR / export_file)
    print(f"export: exported {message}.")


def reload_xrdb(export_file):
    """Merge the colors into the X db so new terminals use them."""
    if shutil.which("xrdb"):
        subprocess.call(["xrdb", "-merge", CACHE_DIR / export_file])


def reload_i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown("i3-msg", "reload")


def export_colors(colors):
    """Export colors in various formats."""
    plain_colors = format_colors.plain(colors)
    save_colors(plain_colors, "colors", "plain hex colors")

    # Shell based colors.
    shell_colors = format_colors.shell(colors)
    save_colors(shell_colors, "colors.sh", "shell variables")

    # Web based colors.
    css_colors = format_colors.css(colors)
    save_colors(css_colors, "colors.css", "css variables")
    scss_colors = format_colors.scss(colors)
    save_colors(scss_colors, "colors.scss", "scss variables")

    # Text editor based colors.
    putty_colors = format_colors.putty(colors)
    save_colors(putty_colors, "colors-putty.reg", "putty theme")

    # X based colors.
    xrdb_colors = format_colors.xrdb(colors)
    save_colors(xrdb_colors, "xcolors", "xrdb colors")

    # i3 colors.
    reload_xrdb("xcolors")
    reload_i3()
