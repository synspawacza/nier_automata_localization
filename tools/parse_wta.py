#!/usr/bin/python3

import argparse
import os
from wtafile import WtaFile

parser = argparse.ArgumentParser()
parser.add_argument("wta_file", help=".wta file name")
parser.add_argument("wtp_file", help=".wtp file name")
parser.add_argument("directory", help="output directory")

args = parser.parse_args()
wta_file = open(args.wta_file, "rb")
wtp_file = open(args.wtp_file, "rb")

wta = WtaFile(wta_file)

for id, f in enumerate(wta.textures):
    out_filename = os.path.basename(args.wta_file)+'_'+str(id).zfill(3)+'.dds'
    with open(os.path.join(args.directory, out_filename), "wb") as out_file:
        wtp_file.seek(f.offset)
        content = wtp_file.read(f.size)
        out_file.write(content)