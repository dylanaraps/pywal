"""
Convert colors to various formats.
"""
from pywal import util


def plain(colors):
    """Convert colors to plain hex."""
    return [f"{color}\n" for color in colors["colors"].values()]


def shell(colors):
    """Convert colors to shell variables."""
    return [f"color{index}='{color}'\n"
            for index, color in enumerate(colors["colors"].values())]


def css(colors):
    """Convert colors to css variables."""
    css_colors = [":root {\n"]
    css_colors.extend([f"\t--color{index}: {color};\n"
                       for index, color in
                       enumerate(colors["colors"].values())])
    css_colors.append("}\n")
    return css_colors


def scss(colors):
    """Convert colors to scss variables."""
    return [f"$color{index}: {color};\n"
            for index, color in enumerate(colors["colors"].values())]


def putty(colors):
    """Convert colors to putty theme."""
    rgb = util.hex_to_rgb
    putty_colors = [
        "Windows Registry Editor Version 5.00\n\n",
        "[HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\Sessions\\Wal]\n",
    ]
    putty_colors.extend([f"\"colour{index}\"=\"{rgb(color)}\"\n"
                         for index, color in
                         enumerate(colors["colors"].values())])

    return putty_colors


def xrdb(colors):
    """Convert colors to xrdb format."""
    x_colors = []
    x_colors.append(f"URxvt*foreground:  {colors['special']['foreground']}\n")
    x_colors.append(f"XTerm*foreground:  {colors['special']['foreground']}\n")
    x_colors.append(f"URxvt*background:  {colors['special']['background']}\n")
    x_colors.append(f"XTerm*background:  {colors['special']['background']}\n")
    x_colors.append(f"URxvt*cursorColor: {colors['special']['cursor']}\n")
    x_colors.append(f"XTerm*cursorColor: {colors['special']['cursor']}\n")

    # Colors 0-15.
    x_colors.extend([f"*.color{index}: {color}\n*color{index}:  {color}\n"
                     for index, color in enumerate(colors["colors"].values())])

    x_colors.append(f"*.color66: {colors['special']['background']}\n"
                    f"*color66:  {colors['special']['background']}\n")

    # Rofi colors.
    x_colors.append(f"rofi.color-window: "
                    f"{colors['special']['background']}, "
                    f"{colors['special']['background']}, "
                    f"{colors['colors']['color10']}\n")
    x_colors.append(f"rofi.color-normal: "
                    f"{colors['special']['background']}, "
                    f"{colors['special']['foreground']}, "
                    f"{colors['special']['background']}, "
                    f"{colors['colors']['color10']}, "
                    f"{colors['special']['background']}\n")
    x_colors.append(f"rofi.color-active: "
                    f"{colors['special']['background']}, "
                    f"{colors['special']['foreground']}, "
                    f"{colors['special']['background']}, "
                    f"{colors['colors']['color10']}, "
                    f"{colors['special']['background']}\n")
    x_colors.append(f"rofi.color-urgent: "
                    f"{colors['special']['background']}, "
                    f"{colors['colors']['color9']}, "
                    f"{colors['special']['background']}, "
                    f"{colors['colors']['color9']}, "
                    f"{colors['special']['foreground']}\n")

    # Emacs colors.
    x_colors.append(f"emacs*background: {colors['special']['background']}\n")
    x_colors.append(f"emacs*foreground: {colors['special']['foreground']}\n")
    return x_colors
