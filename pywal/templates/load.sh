echo -en "{color0.sequences}"

[[ -z "$VTE_VERSION" ]] && \
    echo -en "\\033]708;{color0}\\007"
