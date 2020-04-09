#!/usr/bin/python3

import argparse
from ktbfile import KtbFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".ktb file name")

args = parser.parse_args()
file = open(args.file, "rb")

ktb = KtbFile(file)

#replacement_text = ['Translation.',
#                    'Translation?',
#                    'Translation!']
#
#for i, str in enumerate(replacement_text):
#    ktb.entries[i].text = str

print(ktb.serialize().hex())