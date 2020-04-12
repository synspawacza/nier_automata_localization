#!/usr/bin/python3

import argparse
import os
import format.dat as dat

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help=".dat or .dtt file name")
parser.add_argument("output_file", help="output .dat or .dtt file name")
parser.add_argument("replacement_files", help="files to replace in ", nargs="+")


args = parser.parse_args()

file = open(args.input_file, "rb")
dat = dat.File.parse(file)

for f in dat.files:
    for replacement_file in args.replacement_files:
        if os.path.basename(replacement_file) == f.name:
            f.bytes = open(replacement_file, "rb").read()

out_file = open(args.output_file, "wb")
out_file.write(dat.serialize())
