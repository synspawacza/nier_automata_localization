#!/usr/bin/python3

import argparse
from ftbfile import FtbFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".ftb file name")

args = parser.parse_args()
file = open(args.file, "rb")

ftb = FtbFile(file)

for c in ftb.chars:
    print(vars(c))