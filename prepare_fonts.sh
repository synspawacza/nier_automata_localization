#!/bin/bash

echo "Extracting fonts - it will take several minutes"
echo "Extracting fonts from ftb files"
for font in 00 01 04 05 11
do
    ftb=unpacked/font/font_${font}.dat/font_${font}.ftb
    textures=unpacked/font/font_${font}.dtt/font_${font}.wtp_*
    out_dir=fonts/${font}
    ./tools/unpack_font.py --skip-cjk ${ftb} ${out_dir} ${textures}
done

function extract_mcd() {
    mcd=$1
    font=$2
    echo "Extracting font ${font} from ${mcd}"
    texture=`echo $mcd | sed -e 's/\.dat/.dtt/' -e 's/\.mcd/.wtp_000.dds/'`
    out_dir=fonts/${font}
    ./tools/unpack_font.py --font-id ${font} --skip-cjk ${mcd} ${out_dir} ${texture}
}

function extract_mcd_with_cjk() {
    mcd=$1
    font=$2
    echo "Extracting font ${font} from ${mcd}"
    texture=`echo $mcd | sed -e 's/\.dat/.dtt/' -e 's/\.mcd/.wtp_000.dds/'`
    out_dir=fonts/${font}
    ./tools/unpack_font.py --font-id ${font} ${mcd} ${out_dir} ${texture}
}

for lang in "" "_us" "_fr" "_it" "_de" "_es"
do
    extract_mcd unpacked/ui/ui_title${lang}.dat/messtitle.mcd 02
    extract_mcd unpacked/ui/ui_core${lang}.dat/messcore.mcd 02
    extract_mcd unpacked/ui/ui_shop${lang}.dat/messshop.mcd 02
    extract_mcd unpacked/ui/ui_hud${lang}.dat/messhud.mcd 02
    extract_mcd unpacked/ui/ui_hud_hacking${lang}.dat/messhud_hacking.mcd 02
    extract_mcd unpacked/ui/ui_chapter${lang}.dat/messchapter.mcd 02
    extract_mcd unpacked/ui/ui_ending${lang}.dat/messending.mcd 02
    extract_mcd unpacked/ui/ui_dlc1${lang}.dat/messdlc1.mcd 02
    extract_mcd unpacked/ui/ui_option${lang}.dat/messoption.mcd 02
    extract_mcd unpacked/ui/ui_core${lang}.dat/messcore.mcd 03
    extract_mcd unpacked/ui/ui_dlc1${lang}.dat/messdlc1.mcd 03
    extract_mcd unpacked/ui/ui_ending${lang}.dat/messending.mcd 03
    extract_mcd unpacked/ui/ui_pause${lang}.dat/messpause.mcd 08
    extract_mcd unpacked/ui/ui_core${lang}.dat/messcore.mcd 09
    extract_mcd unpacked/ui/ui_core_2${lang}.dat/messcore_2.mcd 09
    extract_mcd unpacked/ui/ui_dbg${lang}.dat/messdbg.mcd 10
done
extract_mcd_with_cjk unpacked/ui/ui_loading.dat/messloading.mcd 01
extract_mcd_with_cjk unpacked/ui/ui_loading.dat/messloading.mcd 02
extract_mcd_with_cjk unpacked/ui/ui_loading.dat/messloading.mcd 05
./tools/unpack_font.py --char $((16#2514)) --font-id 36 unpacked/ui/ui_chapter_us.dat/messchapter.mcd fonts/01 unpacked/ui/ui_chapter_us.dtt/messchapter.wtp_000.dds
./tools/unpack_font.py --char $((16#251c)) --font-id 36 unpacked/ui/ui_chapter_us.dat/messchapter.mcd fonts/01 unpacked/ui/ui_chapter_us.dtt/messchapter.wtp_000.dds

./tools/unpack_font.py --char $((16#300a)) --font-id 36 unpacked/ui/ui_core_us.dat/messcore.mcd fonts/01 unpacked/ui/ui_core_us.dtt/messcore.wtp_000.dds
./tools/unpack_font.py --char $((16#300b)) --font-id 36 unpacked/ui/ui_core_us.dat/messcore.mcd fonts/01 unpacked/ui/ui_core_us.dtt/messcore.wtp_000.dds
./tools/unpack_font.py --char $((16#300e)) --font-id 36 unpacked/ui/ui_core_us.dat/messcore.mcd fonts/01 unpacked/ui/ui_core_us.dtt/messcore.wtp_000.dds
./tools/unpack_font.py --char $((16#300f)) --font-id 36 unpacked/ui/ui_core_us.dat/messcore.mcd fonts/01 unpacked/ui/ui_core_us.dtt/messcore.wtp_000.dds

./tools/unpack_font.py --char $((16#65e5)) --font-id 1 unpacked/ui/ui_option_us.dat/messoption.mcd fonts/01 unpacked/ui/ui_option_us.dtt/messoption.wtp_000.dds
./tools/unpack_font.py --char $((16#672c)) --font-id 1 unpacked/ui/ui_option_us.dat/messoption.mcd fonts/01 unpacked/ui/ui_option_us.dtt/messoption.wtp_000.dds
./tools/unpack_font.py --char $((16#8a9e)) --font-id 1 unpacked/ui/ui_option_us.dat/messoption.mcd fonts/01 unpacked/ui/ui_option_us.dtt/messoption.wtp_000.dds

