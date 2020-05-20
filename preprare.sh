#!/bin/bash

echo "Unpacking dat files"
./tools/unpack_dat.py data unpacked

echo "Extracting fonts - it will take several minutes"
echo "Extracting fonts from ftb files"
for font in 00 01 04 05 11
do
    ftb=unpacked/font/font_${font}.dat/font_${font}.ftb
    textures=unpacked/font/font_${font}.dtt/font_${font}.wtp_*
    out_dir=fonts/fnt_${font}
    ./tools/unpack_font.py --skip-cjk ${ftb} ${out_dir} ${textures}
done

for lang in "" "_us" "_fr" "_it" "_de" "_es"
do
    mcds=(
    unpacked/ui/ui_loading.dat/messloading.mcd
    unpacked/ui/ui_title${lang}.dat/messtitle.mcd
    unpacked/ui/ui_option${lang}.dat/messoption.mcd
    unpacked/ui/ui_core_pc${lang}.dat/messcore_pc.mcd
    unpacked/ui/ui_core${lang}.dat/messcore.mcd
    unpacked/ui/ui_core_2${lang}.dat/messcore_2.mcd
    unpacked/ui/ui_pause${lang}.dat/messpause.mcd
    unpacked/ui/ui_shop${lang}.dat/messshop.mcd
    unpacked/ui/ui_hud${lang}.dat/messhud.mcd
    unpacked/ui/ui_hud_hacking${lang}.dat/messhud_hacking.mcd
    unpacked/ui/ui_event${lang}.dat/messevent.mcd
    unpacked/ui/ui_credit${lang}.dat/messcredit.mcd
    unpacked/ui/ui_dbg${lang}.dat/messdbg.mcd
    unpacked/ui/ui_chapter${lang}.dat/messchapter.mcd
    unpacked/ui/ui_ending${lang}.dat/messending.mcd
    unpacked/ui/ui_dlc1${lang}.dat/messdlc1.mcd
    unpacked/ui/ui_dlc2${lang}.dat/messdlc2.mcd
    unpacked/ui/ui_dlc3${lang}.dat/messdlc3.mcd
    unpacked/ui/ui_ending_dlc${lang}.dat/messending_dlc.mcd
    )
    for mcd in ${mcds[*]}
    do
        echo "Extracting fonts from $mcd"
        texture=`echo $mcd | sed -e 's/\.dat/.dtt/' -e 's/\.mcd/.wtp_000.dds/'`
        for font in 01 02 03 04 05 06 07 08 09 10 11 35 36 37
        do
            out_dir=fonts/mcd_${font}
            ./tools/unpack_font.py --font-id ${font} --skip-cjk ${mcd} ${out_dir} ${texture}
        done
    done
done

#TODO: get_strings
