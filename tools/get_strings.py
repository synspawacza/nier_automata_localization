#!/usr/bin/python3

import argparse
import os

import format.smd as smd
import format.tmd as tmd
import format.bin as bin
import format.mcd as mcd
import format.properties as properties

parser = argparse.ArgumentParser()
parser.add_argument("input", help="source file name")
parser.add_argument("output", help="target file name (*.properties)")

args = parser.parse_args()
file_ext = os.path.splitext(args.input)[1]

parsed = None
with open(args.input, "rb") as in_file:
    if file_ext == ".bin":
        parsed = bin.File.parse(in_file)
    elif file_ext == ".smd":
        parsed = smd.File.parse(in_file)
    elif file_ext == ".tmd":
        parsed = tmd.File.parse(in_file)
    elif file_ext == ".mcd":
        parsed = mcd.File.parse(in_file)
    else:
        raise Exception("Unable to extract " + args.input + ": unknown file extenstion")

with open(args.output, "wb") as out_file:
    out_file.write(properties.serialize_properties(parsed.get_strings()))
