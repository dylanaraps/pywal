"""
Convert colors to various formats.
"""
from pywal import util


def plain(colors):
    """Convert colors to plain hex."""
    return [f"{color}\n" for color in colors]


def shell(colors):
    """Convert colors to shell variables."""
    return [f"color{index}='{color}'\n"
            for index, color in enumerate(colors)]


def css(colors):
    """Convert colors to css variables."""
    css_colors = [":root {\n"]
    css_colors.extend([f"\t--color{index}: {color};\n"
                       for index, color in enumerate(colors)])
    css_colors.append("}\n")
    return css_colors


def scss(colors):
    """Convert colors to scss variables."""
    return [f"$color{index}: {color};\n"
            for index, color in enumerate(colors)]


def putty(colors):
    """Convert colors to putty theme."""
    rgb = util.hex_to_rgb
    putty_colors = [
        "Windows Registry Editor Version 5.00\n\n",
        "[HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\Sessions\\Wal]\n",
    ]
    putty_colors.extend([f"\"colour{index}\"=\"{rgb(color)}\"\n"
                         for index, color in enumerate(colors)])

    return putty_colors


def xrdb(colors):
    """Convert colors to xrdb format."""
    x_colors = []
    x_colors.append(f"URxvt*foreground:  {colors[15]}\n")
    x_colors.append(f"XTerm*foreground:  {colors[15]}\n")
    x_colors.append(f"URxvt*background:  {colors[0]}\n")
    x_colors.append(f"XTerm*background:  {colors[0]}\n")
    x_colors.append(f"URxvt*cursorColor: {colors[15]}\n")
    x_colors.append(f"XTerm*cursorColor: {colors[15]}\n")

    # Colors 0-15.
    x_colors.extend([f"*.color{index}: {color}\n*color{index}: {color}\n"
                     for index, color in enumerate(colors)])

    x_colors.append(f"*.color66: {colors[0]}\n*color66: {colors[0]}\n")

    # Rofi colors.
    x_colors.append(f"rofi.color-window: {colors[0]}, "
                    f"{colors[0]}, {colors[10]}\n")
    x_colors.append(f"rofi.color-normal: {colors[0]}, "
                    f"{colors[15]}, {colors[0]}, "
                    f"{colors[10]}, {colors[0]}\n")
    x_colors.append(f"rofi.color-active: {colors[0]}, "
                    f"{colors[15]}, {colors[0]}, "
                    f"{colors[10]}, {colors[0]}\n")
    x_colors.append(f"rofi.color-urgent: {colors[0]}, "
                    f"{colors[9]}, {colors[0]}, "
                    f"{colors[9]}, {colors[15]}\n")

    # Emacs colors.
    x_colors.append(f"emacs*background: {colors[0]}\n")
    x_colors.append(f"emacs*foreground: {colors[15]}\n")
    return x_colors
