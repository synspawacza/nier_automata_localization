#!/usr/bin/python3

import argparse
from tmdfile import TmdFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".tmd file name")

args = parser.parse_args()
file = open(args.file, "rb")

tmd = TmdFile(file)

#replacement_text = ['Translation.',
#                    'Translation?',
#                    'Translation!']
#
#for i, str in enumerate(replacement_text):
#    tmd.entries[i].text = str

print(tmd.serialize().hex())