"""
Export colors in various formats.
"""
import shutil
import subprocess

from pywal import globals as g
from pywal import util


def save_colors(colors, export_file, message):
    """Export colors to var format."""
    colors = "\n".join(colors)
    util.save_file(f"{colors}\n", g.CACHE_DIR / export_file)
    print(f"export: exported {message}.")


def reload_xrdb(export_file):
    """Merge the colors into the X db so new terminals use them."""
    if shutil.which("xrdb"):
        subprocess.call(["xrdb", "-merge", g.CACHE_DIR / export_file])


def reload_i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown("i3-msg", "reload")


def export_rofi(colors):
    """Append rofi colors to the x_colors list."""
    g.ColorType.xrdb.append(f"rofi.color-window: {colors[0]}, "
                            f"{colors[0]}, {colors[10]}")
    g.ColorType.xrdb.append(f"rofi.color-normal: {colors[0]}, "
                            f"{colors[15]}, {colors[0]}, "
                            f"{colors[10]}, {colors[0]}")
    g.ColorType.xrdb.append(f"rofi.color-active: {colors[0]}, "
                            f"{colors[15]}, {colors[0]}, "
                            f"{colors[10]}, {colors[0]}")
    g.ColorType.xrdb.append(f"rofi.color-urgent: {colors[0]}, "
                            f"{colors[9]}, {colors[0]}, "
                            f"{colors[9]}, {colors[15]}")


def export_emacs(colors):
    """Set emacs colors."""
    g.ColorType.xrdb.append(f"emacs*background: {colors[0]}")
    g.ColorType.xrdb.append(f"emacs*foreground: {colors[15]}")


def export_colors(colors):
    """Export colors in various formats."""
    save_colors(g.ColorType.plain, "colors", "plain hex colors")
    save_colors(g.ColorType.shell, "colors.sh", "shell variables")

    # Web based colors.
    g.ColorType.css.append("}")
    save_colors(g.ColorType.css, "colors.css", "css variables")
    save_colors(g.ColorType.scss, "colors.scss", "scss variables")

    # Text editor based colors.
    save_colors(g.ColorType.putty, "colors-putty.reg", "putty theme")

    # X based colors.
    export_rofi(colors)
    export_emacs(colors)
    save_colors(g.ColorType.xrdb, "xcolors", "xrdb colors")

    # i3 colors.
    reload_xrdb("xcolors")
    reload_i3()
