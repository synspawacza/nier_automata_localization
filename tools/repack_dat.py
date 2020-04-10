#!/usr/bin/python3

import argparse
import os
from datarchive import DatArchive

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help=".dat or .dtt file name")
parser.add_argument("replacement_file", help="replacement file name")
parser.add_argument("output_file", help="output .dat or .dtt file name")


args = parser.parse_args()

file = open(args.input_file, "rb")
dat = DatArchive(file)
#out_dir = args.directory
#
#
#for f in dat.files:
#    with open(os.path.join(args.directory, f.name), "wb") as out_file:
#        file.seek(f.offset)
#        content = file.read(f.size)
#        out_file.write(content)

for f in filter(lambda f: f.name == os.path.basename(args.replacement_file), dat.files):
    f.bytes = open(args.replacement_file, "rb").read()

out_file = open(args.output_file, "wb")
out_file.write(dat.serialize())