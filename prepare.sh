#!/bin/bash

echo "Unpacking dat files"
./tools/unpack_dat.py data unpacked

astcenc_tool=./tools/astcenc-avx2
if [[ $OSTYPE == 'cygwin' || $OSTYPE == 'msys' ]]
then astcenc_tool=./tools/astcenc-avx2.exe
fi

for astc_file in `find unpacked/ -name '*.astc'`
do
  dds_file=${astc_file:0:-5}
  ${astcenc_tool} -dl ${astc_file} ${dds_file}
done

./prepare_fonts.sh

./get_strings.sh
