#!/usr/bin/python3

import argparse
import format.wta as wta
from format.utils import *


def repack_wtp(parsed_wta, in_wtp, out_wtp, textures):
    for id, f in enumerate(parsed_wta.textures):
        if id in textures:
            texture = None
            with open(textures[id], "rb") as texture_file:
                texture = texture_file.read()
            f.offset = out_wtp.tell()
            f.size = len(texture)
            out_wtp.write(texture)
            out_wtp.write(write_padding(out_wtp.tell(), 0x1000))
        else:
            in_wtp.seek(f.offset)
            texture = in_wtp.read(f.size)
            f.offset = out_wtp.tell()
            f.size = len(texture)
            out_wtp.write(texture)
            out_wtp.write(write_padding(out_wtp.tell(), 0x1000))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_wta", help="source wta file")
    parser.add_argument("input_wtp", help="source wtp file")
    parser.add_argument("output_wta", help="source wta file")
    parser.add_argument("output_wtp", help="source wtp file")
    parser.add_argument(
        "--texture",
        help="texture id and texture image (must be .dds)",
        metavar=("ID", "TEXTURE"),
        nargs=2,
        action="append",
    )

    args = parser.parse_args()

    textures = {int(id): filename for id, filename in args.texture}

    wta_file = open(args.input_wta, "rb")
    in_wtp = open(args.input_wtp, "rb")
    parsed_wta = wta.File.parse(wta_file)

    out_wtp = open(args.output_wtp, "wb")
    repack_wtp(parsed_wta, in_wtp, out_wtp, textures)
    open(args.output_wta, "wb").write(parsed_wta.serialize())
