"""wal - Export functions."""
import subprocess
import shutil


def plain(colors, export_file):
    """Export colors to a plain text file."""
    with open(export_file, 'w') as file:
        file.write('\n'.join(colors))

    print("export: Exported plain colors.")


def generic(colors, col_format):
    """Export colors to var format."""
    # Loop over the colors and format them.
    colors = [col_format % (num, color) for num, color in enumerate(colors)]
    export_colors = ''.join(colors)

    return export_colors


def save_file(colors, export_file):
    """Write the colors to the file."""
    with open(export_file, 'w') as file:
        file.write(colors)


def shell(colors, export_file):
    """Export colors to shell format."""
    col_format = "color%s='%s'\n"
    export_colors = generic(colors, col_format)
    save_file(export_colors, export_file)

    print("export: Exported shell colors.")


def scss(colors, export_file):
    """Export colors to scss format."""
    col_format = "$color%s: %s;\n"
    export_colors = generic(colors, col_format)
    save_file(export_colors, export_file)

    print("export: Exported scss colors.")


def css(colors, export_file):
    """Export colors to firefox format."""
    col_format = "\t--color%s: %s;\n"
    export_colors = ":root {\n%s}\n" % str(generic(colors, col_format))
    save_file(export_colors, export_file)

    print("export: Exported firefox colors.")


def xrdb_col(key, color):
    """Format xrdb keys."""
    return "%s: %s\n" % (key, color)


def xrdb(colors, export_file):
    """Export colors to xrdb."""

    # Write the colors to the file.
    with open(export_file, 'w') as file:
        file.write(x_colors)

    # Merge the colors into the X db so new terminals use them.
    if shutil.which("xrdb"):
        subprocess.Popen(["xrdb", "-merge", export_file])

    print("export: Exported xrdb colors.")
