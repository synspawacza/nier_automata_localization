#!/usr/bin/python3

import argparse
import format.ftb as ftb
import format.mcd as mcd
from PIL import Image
import os


def ensure_dir(output_dir):
    if os.path.isfile(output_dir):
        raise Exception("Unable to extract to " + output_dir + ": not a directory")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-cjk", help="skip CJK characters", action="store_true")
    parser.add_argument(
        "--font-id", help="font number (relevant for .mcd)", default=0, type=int
    )
    parser.add_argument(
        "--char", help="extract only the character specified by code point", type=int
    )
    parser.add_argument("font_file", help=".ftb or .mcd file name")
    parser.add_argument(
        "directory", help="output directory that will contain separated glyphs"
    )
    parser.add_argument(
        "image_files", help="list of image file names (.dds or .png)", nargs="+"
    )

    args = parser.parse_args()

    parsed = None
    ext = os.path.splitext(args.font_file)[1]
    if ext == ".ftb":
        parsed = ftb.File.parse(open(args.font_file, "rb"))
        if len(args.image_files) != parsed.header.textures_count:
            raise Exception(
                "Invalid number of image files: was {0}, expected {1}".format(
                    len(args.image_files), parsed.header.textures_count
                )
            )
    elif ext == ".mcd":
        parsed = mcd.File.parse(open(args.font_file, "rb"))
        if len(args.image_files) != 1:
            raise Exception(
                "Invalid number of image files: was {0}, expected 1".format(
                    len(args.image_files)
                )
            )
    else:
        raise Exception("Unknown file type for: " + args.font_file)

    textures = []
    for img_file in args.image_files:
        textures.append(Image.open(img_file))

    ensure_dir(args.directory)

    for char, glyph in parsed.get_glyphs(textures, args.font_id).items():
        if args.char and args.char != ord(char):
            continue
        if args.skip_cjk and ord(char) >= 0x2E80 and ord(char) <= 0x9FFF:
            continue
        outfile = os.path.join(args.directory, "{0:04x}.png".format(ord(char)))
        glyph.save(outfile)
