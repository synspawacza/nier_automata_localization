#!/usr/bin/python3

import argparse
from ftbfile import FtbFile
from PIL import Image
import os

parser = argparse.ArgumentParser()
parser.add_argument("--skip_cjk", help="skip CJK characters", action="store_true")
parser.add_argument("ftb_file", help=".ftb file name")
parser.add_argument("directory", help="output directory that will contain separated glyphs")
parser.add_argument("image_files", help="list of image file names (.dds or .png)", nargs='+')

args = parser.parse_args()
file = open(args.ftb_file, "rb")

ftb = FtbFile(file)

if len(args.image_files) != ftb.header.textures_count:
    print("Invalid number of image files: was {0}, expected {1}".format(len(args.image_files), ftb.header.textures_count))
    exit(0)
    
textures = []
for img_file in args.image_files:
    textures.append(Image.open(img_file))

for c in ftb.chars:
    if(c.width == 0 or c.height == 0):
        continue
    if args.skip_cjk and ord(c.char) >= 0x2e80 and ord(c.char) <= 0x9fff:
        continue
    textures[c.texture_id].crop((c.u, c.v, c.u+c.width, c.v+c.height)).save(os.path.join(args.directory,'{:04x}.png'.format(ord(c.char))))