#!/usr/bin/python3

import argparse
from ftbfile import FtbFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".ftb file name")

args = parser.parse_args()
file = open(args.file, "rb")

ftb = FtbFile(file)

#replacement_text = ['Translation.',
#                    'Translation?',
#                    'Translation!']
#
#for i, str in enumerate(replacement_text):
#    ftb.entries[i].text = str

print(ftb.serialize().hex())