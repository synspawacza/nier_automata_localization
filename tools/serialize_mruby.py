#!/usr/bin/python3

import argparse
from mrubybytecode import MrubyFile
from mrubybytecode import UnknownSection

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".bin file name")

args = parser.parse_args()
file = open(args.file, "rb")

mruby = MrubyFile(file)

print(mruby.serialize().hex())