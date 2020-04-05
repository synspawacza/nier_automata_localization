#!/usr/bin/python3

import argparse
from smdfile import SmdFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".smd file name")

args = parser.parse_args()
file = open(args.file, "rb")

smd = SmdFile(file)

#replacement_text = ['Translation.',
#                    'Translation?',
#                    'Translation!']
#
#for i, str in enumerate(replacement_text):
#    smd.entries[i].text = str

print(smd.serialize().hex())