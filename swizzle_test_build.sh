#!/bin/bash

#parameters:
USE_OG_ASTC=1 #0
BLOCK_SIZE=6 #4 8
FORMAT_ID=0x7d #0x79
PADDING=0 #360448
#end parameters

# ASTC (weird texture formats ??)
# 0x2D: "ASTC_4x4_UNORM",
# 0x38: "ASTC_8x8_UNORM",
# 0x3A: "ASTC_12x12_UNORM",
# ASTC
# 0x79: "ASTC_4x4_UNORM",
# 0x80: "ASTC_8x8_UNORM",
# 0x87: "ASTC_4x4_SRGB",
# 0x8E: "ASTC_8x8_SRGB",
# Unknown NieR switch formats
# 0x79: "ASTC_4x4_UNORM",
# 0x7D: "ASTC_6x6_UNORM",
# 0x8B: "ASTC_6x6_SRGB",

astcenc_tool=./tools/astcenc-avx2
if [[ $OSTYPE == 'cygwin' || $OSTYPE == 'msys' ]]
then astcenc_tool=./tools/astcenc-avx2.exe
fi

DAT_FILE=ui/ui_title_us.dat
NAME=messtitle
DTT_FILE=${DAT_FILE/.dat/.dtt}

mkdir -p assembly/${DAT_FILE}/
mkdir -p assembly/${DTT_FILE}/

if [ $USE_OG_ASTC -eq 1 ]
then
    cp unpacked/${DTT_FILE}/${NAME}.wtp_000.dds.astc assembly/${DTT_FILE}/${NAME}.wtp_000.astc
else
    ${astcenc_tool} -cl unpacked/${DTT_FILE}/${NAME}.wtp_000.dds assembly/${DTT_FILE}/${NAME}.wtp_000.astc ${BLOCK_SIZE}x${BLOCK_SIZE} -thorough
fi

./tools/repack_wtp.py unpacked/${DAT_FILE}/${NAME}.wta unpacked/${DTT_FILE}/${NAME}.wtp assembly/${DAT_FILE}/${NAME}.wta assembly/${DTT_FILE}/${NAME}.wtp --texture 0 assembly/${DTT_FILE}/${NAME}.wtp_000.astc --block_size ${BLOCK_SIZE} --format_id ${FORMAT_ID} --texture_padding ${PADDING}

mkdir -p `dirname output/${DAT_FILE}`
mkdir -p `dirname output/${DTT_FILE}`
./tools/repack_dat.py data/${DAT_FILE} output/${DAT_FILE} assembly/${DAT_FILE}/${NAME}.wta
./tools/repack_dat.py data/${DTT_FILE} output/${DTT_FILE} assembly/${DTT_FILE}/${NAME}.wtp
