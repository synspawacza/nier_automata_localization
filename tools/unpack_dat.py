#!/usr/bin/python3

import argparse
import os
import format.dat as dat

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".dat or .dtt file name")
parser.add_argument("directory", help="output directory")

args = parser.parse_args()
file = open(args.file, "rb")
out_dir = args.directory

dat = dat.File.parse(file)

for f in dat.files:
    with open(os.path.join(args.directory, f.name), "wb") as out_file:
        out_file.write(f.bytes)
