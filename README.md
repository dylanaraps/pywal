# wal (Python 3 version)

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md) [![Build Status](https://travis-ci.org/dylanaraps/wal.py.svg?branch=master)](https://travis-ci.org/dylanaraps/wal.py)

`wal` is a script that takes an image (or a directory of images), generates a colorscheme (using `imagemagick`) and then changes all of your open terminal's colorschemes to the new colors on the fly. `wal` then caches each generated colorscheme so that cycling through wallpapers while changing colorschemes is instantaneous. `wal` finally merges the new colorscheme into the Xresources db so that any new terminal emulators you open use the new colorscheme.

`wal` can also change the colors in some other programs, check out the [Customization](#customization) section below.

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
* [Plugins](#plugins)
    * [Hyper Terminal](#hyper-terminal)
* [Customization](#customization)
    * [i3](#i3)
    * [rofi](#rofi)
    * [vim](#vim)
    * [Emacs](#emacs)
    * [polybar](#polybar)
    * [iTerm2](#iterm2)
    * [Shell Variables](#shell-variables)
    * [SCSS variables](#scss-variables)
    * [CSS variables](#css-variables)
    * [PuTTY](#putty)
    * [Scripting](#scripting)
    * [Terminal.sexy](#terminalsexy)

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


## Plugins

Listed below are plugins for other programs that add support for `wal` colors.

### Hyper Terminal

https://github.com/dneustadt/hyper-wal



## Customization

I've written another script \[1\] for personal use only that updates my `lemonbar`, `dunst` and `startpage` colors with the new ones from `wal` when run.

What I've done is bind both `wal` and my custom script to the same key so that after `wal` has done its thing my custom script applies the colors to the rest of my environment.

```sh
# i3 config.
# ...

# Cycle wallpapers and apply new colorscheme.
bindsym $mod+w exec "wal -i $HOME/Pictures/Wallpapers -o wal-set"
```

Now whenever I press `Win+w` a random wallpaper is chosen and all of the programs on my system start using the new colors immediately.

I've also set `wal` and my custom script to start with X. This means that when I boot my PC a random wallpaper is chosen and colors are generated + applied to all of my programs.

```sh
# .xinitrc
wal -i "$HOME/Pictures/Wallpapers" -o wal-set
exec i3
```

Have a look at my script to see how `wal` is used and how the programs get reloaded with the new colors.

\[1\] https://github.com/dylanaraps/bin/blob/master/wal-set

**NOTE:** `wal` stores the exported files in `$HOME/.cache/wal/`


### i3

To use `wal` with i3 you have to make some modifications to your i3 config file.

i3 can read colors from `Xresources` into config variables! This allows us to change i3's colors dynamically. On run `wal` will detect that you're running i3 and reload your config for you. If you've set it up correctly i3 will then use your new colorscheme.

Example:

```sh
# Set colors from Xresources
# Change 'color7' and 'color2' to whatever colors you want i3 to use
# from the generated scheme.
# NOTE: The '#f0f0f0' in the lines below is the color i3 will use if
# it fails to get colors from Xresources for some reason.
set_from_resource $fg i3wm.color7 #f0f0f0
set_from_resource $bg i3wm.color2 #f0f0f0

# class                 border  backgr. text indicator child_border
client.focused          $bg     $bg     $fg  $bg       $bg
client.focused_inactive $bg     $bg     $fg  $bg       $bg
client.unfocused        $bg     $bg     $fg  $bg       $bg
client.urgent           $bg     $bg     $fg  $bg       $bg
client.placeholder      $bg     $bg     $fg  $bg       $bg

client.background       $bg

# PROTIP: You can also dynamically set dmenu's colors this way:
bindsym $mod+d exec dmenu_run -nb "$fg" -nf "$bg" -sb "$bg" -sf "$fg"
```


### rofi

`wal` updates rofi's colors for you out of the box, automatically.


### vim

Inside this repo there's a colorscheme I created for vim that uses your terminal colors. It was made to work with the colors `wal` generates and you can install it using any vim package manager.

Example:

```vim
! Using plug
Plug 'dylanaraps/wal'

colorscheme wal
```

### Emacs

Install [this package](https://github.com/cqql/xresources-theme), which will make Emacs use your X environment's colors instead of its default colors.

### polybar

Polybar can read colors from `Xresources` to set the bar's colors.

Example:

```vim
fg = ${xrdb:color7}
bg = ${xrdb:color2}
```

### iTerm2

There's a script called `wal2iterm` in `contrib/wal2iterm` which converts the generated colors to an importable iTerm2 colorscheme.

The themes are stored in the `wal` cache directory. (`${HOME}/.cache/wal/itermcolors`).

Example:

```sh
wal -i "IMAGE" -o "/path/to/wal2iterm/wal2iterm"
```


### Shell Variables

`wal` also exports the colorscheme as a list of shell variables that you can source for use in scripts and the shell.

Example:

```sh
# Add this line to your .bashrc or a shell script.
source "$HOME/.cache/wal/colors.sh"

```

In the shell:

```sh
# Once the file is sourced you can use the colors like this:

dylan ~ >echo "$color0"
#282A23

dylan ~ >echo "$color0 $color5"
#282A23 #BCC3CE

# lemonbar example
lemonbar -B "$color7" -F "$color0"
```


### SCSS variables

`wal` also exports the colorscheme as SCSS variables for use in webpages. I'm using this feature to update my startpage with the new colors dynamically.

Example:

```scss
// Example .scss file

// Import Colors
@import '/home/dylan/.cache/wal/colors.scss';

body {
    background: $color0;
    color: $color7;
}
```

### CSS variables

`wal` also exports the colors as CSS variables for use with Stylish or userChrome.css.

Example CSS:

```css
/* Import the CSS file.
   NOTE: This must be at line 1 of your stylesheet. */
@import url('file:///home/dylan/.cache/wal/firefox.css')

/* Use the variables */
#nav-bar {
    background-color: var(--color3) !important;
    color: var(--color7) !important;
}

```

### PuTTY

`wal` also exports the colors so they can be used with PuTTY. After running `wal`, a file will be created (`$HOME/.cache/wal/colors-putty.reg`) that can be executed on a Windows machine to create a new PuTTY session with the generated colors. Once the file is executed, you can select `Wal` from the *Saved Sessions* list.


### Scripting

`wal` also exports the colors in a plain text format. This is helpful when you want use the plain colors in another script. See the script in `contrib/wal2iterm` for an example.

The file is called `colors` and just contains the hex values one per line in the order of 0-15.

Example `colors` file:

```
#0C2B32
#9C7648
#B78742
#B4884D
#AC8C64
#D19D62
#61828A
#F0DEC0
#666666
#9C7648
#B78742
#B4884D
#AC8C64
#D19D62
#61828A
#F0DEC0
```

Example usage in a script:

```sh
# Create an array with the plain hex colors ordered 0-15.
c=($(< "${cache_dir}/colors"))

# Remove the leading '#' if needed.
c=("${c[@]//\#}")
```

### Terminal.sexy

You can import `wal`'s colors into Terminal.sexy by copy-pasting the contents of the `xcolors` file located in the cache directory.
