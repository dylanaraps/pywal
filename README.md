# wal (Python 3 version)

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md) [![Build Status](https://travis-ci.org/dylanaraps/wal.py.svg?branch=master)](https://travis-ci.org/dylanaraps/wal.py)

`wal` is a script that takes an image (or a directory of images), generates a colorscheme (using `imagemagick`) and then changes all of your open terminal's colorschemes to the new colors on the fly. `wal` then caches each generated colorscheme so that cycling through wallpapers while changing colorschemes is instantaneous. `wal` finally merges the new colorscheme into the Xresources db so that any new terminal emulators you open use the new colorscheme.

`wal` can also change the colors in some other programs, check out the [WIKI](https://github.com/dylanaraps/wal.py/wiki).

**NOTE:** `wal` is not perfect and won't work with some images.

[Albums of examples (Warning large)](https://dylanaraps.com/pages/rice)

![screen](http://i.imgur.com/4aLsvvW.png)


## Table of Contents

<!-- vim-markdown-toc GFM -->
* [Requirements](#requirements)
    * [Dependencies](#dependencies)
    * [Terminal Emulator](#terminal-emulator)
* [Installation](#installation)
    * [Pip install](#pip-install)
    * [Manual install](#manual-install)
* [Setup](#setup)
    * [Applying the theme to new terminals.](#applying-the-theme-to-new-terminals)
    * [Making the colorscheme persist on reboot.](#making-the-colorscheme-persist-on-reboot)
* [Usage](#usage)
* [Customization](#customization)

<!-- vim-markdown-toc -->


## Requirements


### Dependencies

- `python 3.6`
- `imagemagick`
    - Colorscheme generation
- `xfce`, `gnome`, `cinnamon`, `mate`
    - Desktop wallpaper setting.
- `feh`, `nitrogen`, `bgs`, `hsetroot`, `habak`
    - Universal wallpaper setting.


### Terminal Emulator

To use `wal` your terminal emulator must support a special type of escape sequence. The command below can be used as a test to see if `wal` will work with your setup.

Run the command below, does the background color of your terminal become red?

```sh
printf "%b" "\033]11;#ff0000\007"
```

If your terminal's background color is now red, your terminal will work with `wal`.


## Installation


### Pip install

```sh
pip install pywal
```

### Manual install

Just grab the script (`wal`) and add it to your path.


## Setup

**NOTE:** If you get junk in your terminal, add `-t` to all of the `wal` commands.

### Applying the theme to new terminals.

`wal` only applies the new colors to the currently open terminals. Any new terminal windows you open won't be using the new theme unless you add a single line to your shell's start up file. (`.bashrc`, `.zshrc` etc.) The `-r` flags tells `wal` to find the current colorscheme inside the cache and then set it for the new terminal.

Add this line to your shell startup file. (`.bashrc`, `.zshrc` or etc.)

```sh
# Import colorscheme from 'wal'
(wal -r &)
```

Here's how the extra syntax above works:

```sh
&   # Run the process in the background.
( ) # Hide shell job control messages.
```

### Making the colorscheme persist on reboot.

On reboot your new colorscheme won't be set or in use. To fix this you have to add a line to your `.xinitrc` or whatever file starts programs on your system. This `wal` command will set your wallpaper to the wallpaper that was set last boot and also apply the colorscheme again.

Without this you'll be themeless until you run `wal` again on boot.

```sh
# Add this to your .xinitrc or whatever file starts programs on startup.
wal -i "$(< "${HOME}/.cache/wal/wal")"
```


## Usage

Run `wal` and point it to either a directory (`wal -i "path/to/dir"`) or an image (`wal -i "/path/to/img.jpg"`) and that's all. `wal` will change your wallpaper for you and also set your terminal colors.

```sh
usage: wal [-h] [-c] [-i "/path/to/img.jpg"] [-n] [-o "script_name"] [-q] [-r]
           [-t] [-v]

wal - Generate colorschemes on the fly

optional arguments:
  -h, --help            show this help message and exit
  -c                    Delete all cached colorschemes.
  -i "/path/to/img.jpg"
                        Which image or directory to use.
  -n                    Skip setting the wallpaper.
  -o "script_name"      External script to run after "wal".
  -q                    Quiet mode, don"t print anything.
  -r                    Reload current colorscheme.
  -t                    Fix artifacts in VTE Terminals. (Termite,
                        xfce4-terminal)
  -v                    Print "wal" version.

```

## Customization

See the `wal` wiki!

**https://github.com/dylanaraps/wal.py/wiki**
