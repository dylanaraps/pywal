#!/bin/sh
if [ "${{TERM:-none}}" = "linux" ]; then
    printf "%b" "\\e]P0{color0.strip}"
    printf "%b" "\\e]P1{color1.strip}"
    printf "%b" "\\e]P2{color2.strip}"
    printf "%b" "\\e]P3{color3.strip}"
    printf "%b" "\\e]P4{color4.strip}"
    printf "%b" "\\e]P5{color5.strip}"
    printf "%b" "\\e]P6{color6.strip}"
    printf "%b" "\\e]P7{color7.strip}"
    printf "%b" "\\e]P8{color8.strip}"
    printf "%b" "\\e]P9{color9.strip}"
    printf "%b" "\\e]PA{color10.strip}"
    printf "%b" "\\e]PB{color11.strip}"
    printf "%b" "\\e]PC{color12.strip}"
    printf "%b" "\\e]PD{color13.strip}"
    printf "%b" "\\e]PE{color14.strip}"
    printf "%b" "\\e]PF{color15.strip}"

    # Fix artifacting.
    clear
fi
