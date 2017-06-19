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


# wal files.
CACHE_DIR = "%s%s" % (os.path.expanduser("~"), "/.cache/wal/")
SCHEME_DIR = "%s%s" % (CACHE_DIR, "schemes/")
SEQUENCE_FILE = "%s%s" % (CACHE_DIR, "sequences")
WAL_FILE = "%s%s" % (CACHE_DIR, "wal")
PLAIN_FILE = "%s%s" % (CACHE_DIR, "colors")
XRDB_FILE = "%s%s" % (CACHE_DIR, "xcolors")

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

        # Set the wallpaper.
        if not args.n:
            set_wallpaper(image)
    # -f
    elif args.f:
        cache_file = pathlib.Path(args.f)

        # Import the colorscheme from file.
        if cache_file.is_file():
            with open(cache_file) as file:
                colors = file.readlines()

            # Strip newlines from each list element.
            colors = [x.strip() for x in colors]

            if len(colors) < 16:
                print("error: Invalid colorscheme file chosen.")
                exit(1)
        else:
            print("error: Colorscheme file not found.")
            exit(1)

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
        with open(cache_file) as file:
            colors = file.readlines()

        # Strip newlines from each list element.
        colors = [x.strip() for x in colors]
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


def set_special(index, color):
    """Build the escape sequence for special colors."""
    return "\\033]%s;%s\\007" % (str(index), color)


def set_color(index, color):
    """Build the escape sequence we need for each color."""
    return "\\033]4;%s;%s\\007" % (str(index), color)


def get_grey(colors):
    """Set a grey color based on brightness of color0"""
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


def send_sequences(colors, vte):
    """Send colors to all open terminals."""
    seq = []
    seq.append(set_special(10, colors[15]))
    seq.append(set_special(11, colors[0]))
    seq.append(set_special(12, colors[15]))
    seq.append(set_special(13, colors[15]))
    seq.append(set_special(14, colors[0]))

    # This escape sequence doesn't work in VTE terminals.
    if not vte:
        seq.append(set_special(708, colors[0]))

    seq.append(set_color(0, colors[0]))
    seq.append(set_color(1, colors[9]))
    seq.append(set_color(2, colors[10]))
    seq.append(set_color(3, colors[11]))
    seq.append(set_color(4, colors[12]))
    seq.append(set_color(5, colors[13]))
    seq.append(set_color(6, colors[14]))
    seq.append(set_color(7, colors[15]))
    seq.append(set_color(8, get_grey(colors)))
    seq.append(set_color(9, colors[9]))
    seq.append(set_color(10, colors[10]))
    seq.append(set_color(11, colors[11]))
    seq.append(set_color(12, colors[12]))
    seq.append(set_color(13, colors[13]))
    seq.append(set_color(14, colors[14]))
    seq.append(set_color(15, colors[15]))

    # Set a blank color that isn't affected by bold highlighting.
    seq.append(set_color(66, colors[0]))

    # Create the string.
    sequences = ''.join(seq)

    # Decode the string.
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


def export_plain(colors):
    """Export colors to a plain text file."""
    with open(PLAIN_FILE, 'w') as file:
        file.write('\n'.join(colors))


def export_xrdb(colors):
    """Export colors to xrdb."""
    x_colors = """
    URxvt*foreground:  %s
    XTerm*forefround:  %s
    URxvt*background:  %s
    XTerm*background:  %s
    URxvt*cursorColor: %s
    XTerm*cursorColor: %s
    *.color0:  %s
    *.color1:  %s
    *.color2:  %s
    *.color3:  %s
    *.color4:  %s
    *.color5:  %s
    *.color6:  %s
    *.color7:  %s
    *.color8:  %s
    *.color9:  %s
    *.color10: %s
    *.color11: %s
    *.color12: %s
    *.color13: %s
    *.color14: %s
    *.color15: %s
    """ % (colors[15],
           colors[15],
           colors[0],
           colors[0],
           colors[15],
           colors[15],
           colors[0],
           colors[9],
           colors[10],
           colors[11],
           colors[12],
           colors[13],
           colors[14],
           colors[15],
           get_grey(colors),
           colors[9],
           colors[10],
           colors[11],
           colors[12],
           colors[13],
           colors[14],
           colors[15])

    # Write the colors to the file.
    with open(XRDB_FILE, 'w') as file:
        file.write(x_colors)

    # Merge the colors into the X db so new terminals use them.
    subprocess.Popen(["xrdb", "-merge", XRDB_FILE])

    print("export: Exported xrdb colors.")


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
    send_sequences(colors, args.t)
    export_plain(colors)
    export_xrdb(colors)

    # -o
    if args.o:
        subprocess.Popen(["nohup", args.o],
                         stdout=open('/dev/null', 'w'),
                         stderr=open('/dev/null', 'w'),
                         preexec_fn=os.setpgrp)

    return 0


main()
