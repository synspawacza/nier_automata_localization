#!/usr/bin/python3

import argparse
from smdfile import SmdFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".smd file name")

args = parser.parse_args()
file = open(args.file, "rb")

smd = SmdFile(file)

for e in smd.entries:
    print(e.id +'\t' + repr(e.text))