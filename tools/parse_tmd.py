#!/usr/bin/python3

import argparse
from tmdfile import TmdFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".tmd file name")

args = parser.parse_args()
file = open(args.file, "rb")

tmd = TmdFile(file)

for e in tmd.entries:
    print(e.id +'\t' + repr(e.text))