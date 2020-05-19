#!/usr/bin/python3

import argparse
import os
import format.wta as wta


def unpack_wtp(wtp_filename, wta_filename, out_dir=""):
    if not os.path.isfile(wtp_filename) or not os.path.isfile(wta_filename):
        return  # skip if not exist

    with open(wta_filename, "rb") as wta_file:
        with open(wtp_filename, "rb") as wtp_file:
            parsed_wta = wta.File.parse(wta_file)
            for id, f in enumerate(parsed_wta.textures):
                out_filename = wtp_filename + "_" + str(id).zfill(3) + ".dds"
                with open(os.path.join(out_dir, out_filename), "wb") as out_file:
                    wtp_file.seek(f.offset)
                    content = wtp_file.read(f.size)
                    out_file.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wta_file", help=".wta file name")
    parser.add_argument("wtp_file", help=".wtp file name")
    parser.add_argument("directory", help="output directory")

    args = parser.parse_args()
    unpack_wtp(args.wtp_file, args.wta_file, os.path.basename(args.directory))
