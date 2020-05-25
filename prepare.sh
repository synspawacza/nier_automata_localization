#!/bin/bash

echo "Unpacking dat files"
./tools/unpack_dat.py data unpacked

./prepare_fonts.sh

./get_strings.sh
