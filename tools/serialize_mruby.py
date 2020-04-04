#!/usr/bin/python3

import argparse
from mrubybytecode import MrubyFile
from mrubybytecode import PoolRecord
from mrubybytecode import mruby_op_string

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".bin file name")

args = parser.parse_args()
file = open(args.file, "rb")

mruby = MrubyFile(file)

replacement_text = ['Translation.',
                    'Translation?',]
                    'Translation!']
idx = 1
for str in replacement_text:
    mruby.sections[0].segments[1].pool.append(PoolRecord.from_string(str))
    mruby.sections[0].segments[1].instructions[idx]  =mruby_op_string(2, len(mruby.sections[0].segments[1].pool)-1)
    idx += 10

print(mruby.serialize().hex())