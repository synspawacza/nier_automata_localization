#!/usr/bin/python3

import argparse
import os
import format.wta as wta
import swizzle


def unpack_wtp(wtp_filename, wta_filename, out_dir=""):
    if not os.path.isfile(wtp_filename) or not os.path.isfile(wta_filename):
        return  # skip if not exist
    with open(wta_filename, "rb") as wta_file:
        with open(wtp_filename, "rb") as wtp_file:
            parsed_wta = wta.File.parse(wta_file)
            for id, f in enumerate(parsed_wta.textures):
                out_filename = wtp_filename + "_" + str(id).zfill(3) + ".dds"
                if out_dir:
                    out_filename = os.path.join(out_dir, os.path.basename(out_filename))
                if f.is_astc():
                    out_filename = out_filename + ".astc"
                with open(out_filename, "wb") as out_file:
                    wtp_file.seek(f.offset)
                    content = wtp_file.read(f.size)
                    if f.is_astc():
                        size_range = 4 if f.tex_height() >= 512 else 3
                        content = f.astc_header() + swizzle.deswizzle(
                            f.tex_width(),
                            f.tex_height(),
                            6,
                            6,
                            16,
                            0,
                            size_range,
                            content,
                        )
                    out_file.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wta_file", help=".wta file name")
    parser.add_argument("wtp_file", help=".wtp file name")
    parser.add_argument("directory", help="output directory")

    args = parser.parse_args()
    unpack_wtp(args.wtp_file, args.wta_file, args.directory)
