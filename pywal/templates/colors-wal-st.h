static const char *colorname[] = {{
        /* 8 normal colors */
        "{color0}",
        "{color1}",
        "{color2}",
        "{color3}",
        "{color4}",
        "{color5}",
        "{color6}",
        "{color7}",

        /* 8 bright colors */
        "{color8}",
        "{color9}",
        "{color10}",
        "{color11}",
        "{color12}",
        "{color13}",
        "{color14}",
        "{color15}",

        [255] = 0,

        /* more colors can be added after 255 to use with DefaultXX */
        "{background}",
        "{foreground}",
        "{cursor}",
}};


/*
 * Default colors (colorname index)
 * foreground, background, cursor, reverse cursor
 */
unsigned int defaultfg = 257;
unsigned int defaultbg = 256;
static unsigned int defaultcs = 258;
static unsigned int defaultrcs = 258;
