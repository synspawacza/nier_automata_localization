#!/usr/bin/python3

import argparse
import format.wta as wta
from format.utils import *
import swizzle


def repack_wtp(parsed_wta, in_wtp, out_wtp, textures, block_size, format_id, texture_padding):
    for id, f in enumerate(parsed_wta.textures):
        if id in textures:
            texture = None
            with open(textures[id], "rb") as texture_file:
                texture = texture_file.read()
            if f.is_astc():
                size_range = 4 if f.tex_height() >= 512 else 3
                texture = swizzle.swizzle(
                    f.tex_width(), f.tex_height(), block_size, block_size, 16, 0, size_range, texture[16:]
                )
            f.offset = out_wtp.tell()
            f.size = texture_padding if texture_padding > 0 else len(texture)
            if f.is_astc():
                f.update_astc_info(format_id)
            out_wtp.write(texture)
            padding = texture_padding if texture_padding > 0 else 0x1000
            out_wtp.write(write_padding(out_wtp.tell(), padding))
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
    parser.add_argument("--block_size", type=int, help="Block size (default: 4)", default=4, required=False)
    parser.add_argument("--format_id",  type=lambda v: int(v, 0), help="Format ID of ASTC texture (default: 0x79, aka ASTC_4x4_UNORM)", default=0x79, required=False)
    parser.add_argument("--texture_padding", type=int, help="Pad texture to size (default: 0, aka no padding)", default=0, required=False)

    args = parser.parse_args()

    textures = {int(id): filename for id, filename in args.texture}

    wta_file = open(args.input_wta, "rb")
    in_wtp = open(args.input_wtp, "rb")
    parsed_wta = wta.File.parse(wta_file)

    out_wtp = open(args.output_wtp, "wb")
    repack_wtp(parsed_wta, in_wtp, out_wtp, textures, args.block_size, args.format_id, args.texture_padding)
    open(args.output_wta, "wb").write(parsed_wta.serialize())
