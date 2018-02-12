#!/bin/sh
[ "${{TERM:-none}}" = "linux" ] && \
    printf '%b' '\e]P0{color0.strip}
                 \e]P1{color1.strip}
                 \e]P2{color2.strip}
                 \e]P3{color3.strip}
                 \e]P4{color4.strip}
                 \e]P5{color5.strip}
                 \e]P6{color6.strip}
                 \e]P7{color7.strip}
                 \e]P8{color8.strip}
                 \e]P9{color9.strip}
                 \e]PA{color10.strip}
                 \e]PB{color11.strip}
                 \e]PC{color12.strip}
                 \e]PD{color13.strip}
                 \e]PE{color14.strip}
                 \e]PF{color15.strip}
                 \ec'
