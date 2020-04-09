#!/usr/bin/python3

import argparse
from ktbfile import KtbFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".ktb file name")

args = parser.parse_args()
file = open(args.file, "rb")

ktb = KtbFile(file)

for e in ktb.entries:
    print(vars(e))