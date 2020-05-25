#!/bin/bash

function build_font() {
    echo "building font ${1}"

    mkdir -p assembly/font/font_${1}.dat/
    mkdir -p assembly/font/font_${1}.dtt/
    mkdir -p output/font/
    mkdir -p output/font/

    # add ĄąĆćĘęŁłŃńŚśŹźŻż
    ./tools/put_glyphs.py unpacked/font/font_${1}.dat/font_${1}.ftb unpacked/font/font_${1}.dtt/font_${1}.wtp_00${2}.dds \
        assembly/font/font_${1}.dat/font_${1}.ftb assembly/font/font_${1}.dtt/font_${1}.wtp_00${2}.png --page ${2} \
        --char $((16#0104)) fonts/${1}/0104.png \
        --char $((16#0105)) fonts/${1}/0105.png \
        --char $((16#0106)) fonts/${1}/0106.png \
        --char $((16#0107)) fonts/${1}/0107.png \
        --char $((16#0118)) fonts/${1}/0118.png \
        --char $((16#0119)) fonts/${1}/0119.png \
        --char $((16#0141)) fonts/${1}/0141.png \
        --char $((16#0142)) fonts/${1}/0142.png \
        --char $((16#0143)) fonts/${1}/0143.png \
        --char $((16#0144)) fonts/${1}/0144.png \
        --char $((16#015a)) fonts/${1}/015a.png \
        --char $((16#015b)) fonts/${1}/015b.png \
        --char $((16#0179)) fonts/${1}/0179.png \
        --char $((16#017a)) fonts/${1}/017a.png \
        --char $((16#017b)) fonts/${1}/017b.png \
        --char $((16#017c)) fonts/${1}/017c.png

    convert -define dds:mipmaps=0 assembly/font/font_${1}.dtt/font_${1}.wtp_00${2}.png assembly/font/font_${1}.dtt/font_${1}.wtp_00${2}.dds
    
    # add ĄąĆćĘęŃńŚśŹźŻż (skip Ł and ł)
    if [ -e unpacked/font/font_${1}.dat/font_${1}.ktb ]
    then
        ./tools/clone_kernings.py unpacked/font/font_${1}.dat/font_${1}.ktb assembly/font/font_${1}.dat/font_${1}.ktb \
            --char $((16#0041)) $((16#0104)) \
            --char $((16#0061)) $((16#0105)) \
            --char $((16#0043)) $((16#0106)) \
            --char $((16#0063)) $((16#0107)) \
            --char $((16#0045)) $((16#0118)) \
            --char $((16#0065)) $((16#0119)) \
            --char $((16#004E)) $((16#0143)) \
            --char $((16#006E)) $((16#0144)) \
            --char $((16#0053)) $((16#015a)) \
            --char $((16#0073)) $((16#015b)) \
            --char $((16#005A)) $((16#0179)) \
            --char $((16#007A)) $((16#017a)) \
            --char $((16#005A)) $((16#017b)) \
            --char $((16#007A)) $((16#017c))
    fi

    ./tools/repack_wtp.py unpacked/font/font_${1}.dat/font_${1}.wta unpacked/font/font_${1}.dtt/font_${1}.wtp \
        --texture ${2} assembly/font/font_${1}.dtt/font_${1}.wtp_00${2}.dds \
        assembly/font/font_${1}.dat/font_${1}.wta assembly/font/font_${1}.dtt/font_${1}.wtp

    ./tools/repack_dat.py data/font/font_${1}.dat output/font/font_${1}.dat assembly/font/font_${1}.dat/*
    ./tools/repack_dat.py data/font/font_${1}.dtt output/font/font_${1}.dtt assembly/font/font_${1}.dtt/*.wtp
}

build_font 00 0
build_font 01 2
build_font 04 2
build_font 05 2
build_font 11 2
