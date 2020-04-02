#!/usr/bin/python3

import argparse
import os
from datarchive import DatArchive

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".dat or .dtt file name")
parser.add_argument("directory", help="output directory")

args = parser.parse_args()
file = open(args.file, "rb")
out_dir = args.directory

dat = DatArchive(file)

for f in dat.files:
    with open(os.path.join(args.directory, f.name), "wb") as out_file:
        file.seek(f.offset)
        content = file.read(f.size)
        out_file.write(content)