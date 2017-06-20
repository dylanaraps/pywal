#!/usr/bin/env python
"""
wal - Generate and change colorschemes on the fly.
Created by Dylan Araps
"""
import argparse
import glob
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys
from wal import export


# wal files.
CACHE_DIR = "%s%s" % (os.path.expanduser("~"), "/.cache/wal/")
SCHEME_DIR = "%s%s" % (CACHE_DIR, "schemes/")
SEQUENCE_FILE = "%s%s" % (CACHE_DIR, "sequences")
WAL_FILE = "%s%s" % (CACHE_DIR, "wal")

# Internal variables.
COLOR_COUNT = 16


# ARGS {{{


def get_args():
    """Get the script arguments."""
    description = "wal - Generate colorschemes on the fly"
    arg = argparse.ArgumentParser(description=description)

    # Add the args.
    arg.add_argument('-c', action='store_true',
                     help='Delete all cached colorschemes.')

    arg.add_argument('-i', metavar='"/path/to/img.jpg"',
                     help='Which image or directory to use.')

    arg.add_argument('-f', metavar='"/path/to/colors"',
                     help='Load colors directly from a colorscheme file.')

    arg.add_argument('-n', action='store_true',
                     help='Skip setting the wallpaper.')

    arg.add_argument('-o', metavar='"script_name"',
                     help='External script to run after "wal".')

    arg.add_argument('-q', action='store_true',
                     help='Quiet mode, don\'t print anything.')

    arg.add_argument('-r', action='store_true',
                     help='Reload current colorscheme.')

    arg.add_argument('-t', action='store_true',
                     help='Fix artifacts in VTE Terminals. \
                           (Termite, xfce4-terminal)')

    arg.add_argument('-x', action='store_true',
                     help='Use extended 16-color palette.')

    return arg.parse_args()


def process_args(args):
    """Process args"""
    # If no args were passed.
    if not len(sys.argv) > 1:
        print("error: wal needs to be given arguments to run.")
        print("       Refer to 'wal -h' for more info.")
        exit(1)

    # -q
    if args.q:
        sys.stdout = open('/dev/null', 'w')
        sys.stderr = open('/dev/null', 'w')

    # -c
    if args.c:
        shutil.rmtree(SCHEME_DIR)

    # -r
    if args.r:
        reload_colors(args.t)


# }}}


# PROCESS COLORS {{{


def process_colors(args):
    """Process colors."""
    # -i
    if args.i:
        image = str(get_image(args.i))

        # Get the colors.
        colors = get_colors(image)

        # Set Grey.
        if not args.x:
            colors[8] = set_grey(colors)

        # Set the wallpaper.
        if not args.n:
            set_wallpaper(image)
    # -f
    elif args.f:
        cache_file = pathlib.Path(args.f)

        # Import the colorscheme from file.
        if cache_file.is_file():
            colors = read_colors(cache_file)

            if len(colors) < 16:
                print("error: Invalid colorscheme file chosen.")
                exit(1)
        else:
            print("error: Colorscheme file not found.")
            exit(1)

    return colors


def read_colors(color_file):
    """Read colors from a file"""
    with open(color_file) as file:
        colors = file.readlines()

    # Strip newlines from each list element.
    colors = [x.strip() for x in colors]

    return colors


# }}}


# RELOAD COLORS {{{


def reload_colors(vte):
    """Reload colors."""
    with open(SEQUENCE_FILE) as file:
        sequences = file.read()

    # If vte mode was used, remove the problem sequence.
    if vte:
        sequences = re.sub(r'\]708;\#.{6}', '', sequences)

    # Decode the string.
    sequences = bytes(sequences, "utf-8").decode("unicode_escape")

    print(sequences, end='')
    quit()


# }}}


# COLORSCHEME GENERATION {{{


def get_image(img):
    """Validate image input."""
    image = pathlib.Path(img)

    # Check if the user has Imagemagick installed.
    if not shutil.which("convert"):
        print("error: imagemagick not found, exiting...")
        print("error: wal requires imagemagick to function.")
        exit(1)

    if image.is_file():
        wal_img = image

    elif image.is_dir():
        rand = random.choice(os.listdir(image))
        rand_img = "%s/%s" % (str(image), rand)
        rand_img = pathlib.Path(rand_img)

        if rand_img.is_file():
            wal_img = rand_img

    print("image: Using image", wal_img)
    return wal_img


def magic(color_count, img):
    """Call Imagemagick to generate a scheme."""
    colors = subprocess.Popen(["convert", img, "+dither", "-colors",
                               str(color_count), "-unique-colors", "txt:-"],
                              stdout=subprocess.PIPE)

    return colors.stdout.readlines()


def gen_colors(img):
    """Generate a color palette using imagemagick."""
    # Generate initial scheme.
    magic_output = magic(COLOR_COUNT, img)

    # If imagemagick finds less than 16 colors, use a larger source number
    # of colors.
    index = 0
    while len(magic_output) - 1 <= 15:
        index += 1
        magic_output = magic(COLOR_COUNT + index, img)

        print("colors: Imagemagick couldn't generate a", COLOR_COUNT,
              "color palette, trying a larger palette size",
              COLOR_COUNT + index)

    # Remove the first element, which isn't a color.
    del magic_output[0]

    # Create a list of hex colors.
    colors = [re.search('#.{6}', str(col)).group(0) for col in magic_output]
    return colors


def get_colors(img):
    """Generate a colorscheme using imagemagick."""
    # Cache file.
    cache_file = "%s%s" % (SCHEME_DIR, img.replace('/', '_'))
    cache_file = pathlib.Path(cache_file)

    # Cache the wallpaper name.
    with open(WAL_FILE, 'w') as file:
        file.write("%s\n" % (img))

    if cache_file.is_file():
        colors = read_colors(cache_file)

    else:
        print("colors: Generating a colorscheme...")

        # Generate the colors.
        colors = gen_colors(img)

        # Cache the colorscheme.
        with open(cache_file, 'w') as file:
            file.write("\n".join(colors))

    print("colors: Generated colorscheme")
    return colors


# }}}


# SEND SEQUENCES {{{


def send_sequences(colors, vte, extended_palette):
    """Send colors to all open terminals."""
    set_special(10, colors[15])
    set_special(11, colors[0])
    set_special(12, colors[15])
    set_special(13, colors[15])
    set_special(14, colors[0])

    # This escape sequence doesn't work in VTE terminals.
    if not vte:
        set_special(708, colors[0])

    # If -x is used, use all 16 colors.
    if extended_palette:
        set_color(0, colors[0])
        set_color(1, colors[1])
        set_color(2, colors[2])
        set_color(3, colors[3])
        set_color(4, colors[4])
        set_color(5, colors[5])
        set_color(6, colors[6])
        set_color(7, colors[7])
        set_color(8, colors[8])
    else:
        set_color(0, colors[0])
        set_color(1, colors[9])
        set_color(2, colors[10])
        set_color(3, colors[11])
        set_color(4, colors[12])
        set_color(5, colors[13])
        set_color(6, colors[14])
        set_color(7, colors[15])
        set_color(8, colors[8])

    set_color(9, colors[9])
    set_color(10, colors[10])
    set_color(11, colors[11])
    set_color(12, colors[12])
    set_color(13, colors[13])
    set_color(14, colors[14])
    set_color(15, colors[15])

    # Set a blank color that isn't affected by bold highlighting.
    set_color(66, colors[0])

    # Decode the string.
    sequences = ''.join(ColorFormats.sequences)
    sequences = bytes(sequences, "utf-8").decode("unicode_escape")

    # Send the sequences to all open terminals.
    for term in glob.glob("/dev/pts/[0-9]*"):
        with open(term, 'w') as file:
            file.write(sequences)

    # Cache the sequences.
    with open(SEQUENCE_FILE, 'w') as file:
        file.write(sequences)

    print("colors: Set terminal colors")


# }}}


# WALLPAPER SETTING {{{


def set_wallpaper(img):
    """Set the wallpaper."""
    uname = os.uname

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

    elif uname == "Darwin":
        subprocess.Popen(["osascript", "-e", "'tell application \"Finder\" to set \
                           desktop picture to POSIX file\'" + img + "\'"])

    else:
        subprocess.Popen(["gsettings", "set", "org.gnome.desktop.background",
                          "picture-uri", img])

    print("wallpaper: Set the new wallpaper")
    return 0


# }}}


# EXPORT COLORS {{{


class ColorFormats(object):  # pylint: disable=too-few-public-methods
    """Store colors in various formats."""
    x_colors = []
    sequences = []
    plain = []


def set_special(index, color):
    """Build the escape sequence for special colors."""
    ColorFormats.sequences.append("\\033]%s;%s\\007" % (str(index), color))

    if index == 10:
        ColorFormats.x_colors.append("URxvt*foreground: %s\n" % (color))
        ColorFormats.x_colors.append("XTerm*foreground: %s\n" % (color))

    elif index == 11:
        ColorFormats.x_colors.append("URxvt*background: %s\n" % (color))
        ColorFormats.x_colors.append("XTerm*background: %s\n" % (color))

    elif index == 12:
        ColorFormats.x_colors.append("URxvt*cursorColor: %s\n" % (color))
        ColorFormats.x_colors.append("XTerm*cursorColor: %s\n" % (color))


def set_color(index, color):
    """Build the escape sequence we need for each color."""
    ColorFormats.x_colors.append("*.color%s: %s\n" % (str(index), color))
    ColorFormats.sequences.append("\\033]4;%s;%s\\007" % (str(index), color))

    if not index == 66:
        ColorFormats.plain.append(color)


def set_rofi(colors):
    """Append rofi colors to the x_colors list."""
    ColorFormats.x_colors.append("rofi.color-window: %s, %s, %s\n"
                                 % (colors[0], colors[0], colors[10]))
    ColorFormats.x_colors.append("rofi.color-normal: %s, %s, %s, %s, %s\n"
                                 % (colors[0], colors[15], colors[0],
                                    colors[10], colors[0]))
    ColorFormats.x_colors.append("rofi.color-active: %s, %s, %s, %s, %s\n"
                                 % (colors[0], colors[15], colors[0],
                                    colors[10], colors[0]))
    ColorFormats.x_colors.append("rofi.color-urgent: %s, %s, %s, %s, %s\n"
                                 % (colors[0], colors[9], colors[0],
                                    colors[9], colors[15]))


def set_emacs(colors):
    """Set emacs colors."""
    ColorFormats.x_colors.append("emacs*background: %s\n" % (colors[0]))
    ColorFormats.x_colors.append("emacs*foreground: %s\n" % (colors[15]))


def set_grey(colors):
    """Set a grey color based on brightness of color0."""
    return {
        0: "#666666",
        1: "#666666",
        2: "#757575",
        3: "#999999",
        4: "#999999",
        5: "#8a8a8a",
        6: "#a1a1a1",
        7: "#a1a1a1",
        8: "#a1a1a1",
        9: "#a1a1a1",
    }.get(int(colors[0][1]), colors[7])


def export_colors(colors):
    """Call functions to export the colors."""
    set_rofi(colors)
    set_emacs(colors)
    export.plain(ColorFormats.plain, "%s%s" % (CACHE_DIR, "colors"))
    export.xrdb(ColorFormats.x_colors, "%s%s" % (CACHE_DIR, "xcolors"))
    export.scss(ColorFormats.plain, "%s%s" % (CACHE_DIR, "colors.scss"))
    export.shell(ColorFormats.plain, "%s%s" % (CACHE_DIR, "colors.sh"))
    export.css(ColorFormats.plain, "%s%s" % (CACHE_DIR, "colors.css"))


# }}}


def main():
    """Main script function."""
    # Get the args.
    args = get_args()
    process_args(args)

    # Create colorscheme dir.
    pathlib.Path(SCHEME_DIR).mkdir(parents=True, exist_ok=True)

    # Get the colors.
    colors = process_colors(args)

    # Set the colors.
    send_sequences(colors, args.t, args.x)

    # Export the colors.
    export_colors(colors)

    # -o
    if args.o:
        subprocess.Popen(["nohup", args.o],
                         stdout=open('/dev/null', 'w'),
                         stderr=open('/dev/null', 'w'),
                         preexec_fn=os.setpgrp)

    return 0


if __name__ == "__main__":
    main()
