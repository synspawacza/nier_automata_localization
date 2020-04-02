#!/usr/bin/python3

import argparse
from datarchive import DatArchive

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".dat or .dtt file name")

args = parser.parse_args()
file = open(args.file, "rb")

dat = DatArchive(file)

for f in dat.files:
    print(f.name)