#!/usr/bin/python3

import sys

import argparse
import os
import shutil
import format.dat as dat
import unpack_dds


def ensure_dir(output_dir):
    if os.path.isfile(output_dir):
        raise Exception("Unable to extract to " + output_dir + ": not a directory")
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)


def unpack_dat(input_file, output_dir):
    ensure_dir(output_dir)
    with open(input_file, "rb") as file:
        archive = dat.File.parse(file)
        for f in archive.files:
            output_file = os.path.join(output_dir, f.name)
            with open(output_file, "wb") as out_file:
                out_file.write(f.bytes)
            if os.path.splitext(output_file)[1] == ".wtp":
                unpack_dds.unpack_wtp(
                    output_file,
                    output_file.replace(".wtp", ".wta").replace(".dtt", ".dat"),
                    "",
                )


def unpack_dir(input_dir, output_dir, depth):
    if depth <= 0:
        return

    ensure_dir(output_dir)
    for entry in os.scandir(input_dir):
        if entry.is_dir():
            unpack_dir(entry.path, os.path.join(output_dir, entry.name), depth - 1)
        else:
            unpack_file(entry.path, output_dir)


def unpack_file(input_file, output_dir):
    ensure_dir(output_dir)
    ext = os.path.splitext(input_file)[1]
    if ext in {".dat", ".dtt"} and os.path.getsize(input_file) > 0:
        unpack_dat(input_file, os.path.join(output_dir, os.path.basename(input_file)))
    else:
        shutil.copyfile(
            input_file, os.path.join(output_dir, os.path.basename(input_file))
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upacks .dat and .dtt files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    This tool will automatically unpack wta files

    Files will be placed into respecive directories, e.g. for following situation:

    ./dat/
      abc.dat
      abc.dtt
      other.txt

    command `./unpack.py dat out` will create following directory structure:

    ./out/
      abc.dat/
        xyz.bin
        xyz.z
        xyz.wta
      abc.dtt/
        xyz.wtp
        xyz.wtp_001.dds
        xyz.wtp_002.dds
        xyz.wtp_003.dds
      other.txt

    command `./unpack.py dat/abc.dat out` will create following directory structure:

    ./out/
      xyz.bin
      xyz.z
      xyz.wta

    Please note that xyz.wta and xyz.wtp containing texture data will be extracted furher into xyz.wtp_00*.dds files
    """,
    )
    parser.add_argument(
        "--depth", help="recursion depth (default=5)", default=5, type=int
    )
    parser.add_argument("input", help="input file or directory")
    parser.add_argument("output", help="output directory")

    args = parser.parse_args()
    input = args.input
    output = args.output

    if os.path.isfile(output):
        raise Exception(output + " should be a directory")

    if os.path.isfile(input):
        unpack_file(input, output)
    elif os.path.isdir(input):
        unpack_dir(input, output, args.depth)
    else:
        raise Exception(input + " does not exist")
