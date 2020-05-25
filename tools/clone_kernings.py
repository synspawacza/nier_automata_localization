#!/usr/bin/python3

import argparse
import format.ktb as ktb
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="source kerning table file")
    parser.add_argument("output", help="target kerning table file")
    parser.add_argument(
        "--chars",
        help="character id to clone",
        metavar=("FROM", "TO"),
        nargs=2,
        action="append",
    )

    args = parser.parse_args()

    kerning_table = None
    with open(args.input, "rb") as input_ktb:
        kerning_table = ktb.File.parse(input_ktb)

    chars = [(chr(int(c1)), chr(int(c2))) for c1, c2 in args.chars]

    for from_char, to_char in chars:
        kerning_table.clone_kerning(from_char, to_char)
    with open(args.output, "wb") as out_ktb:
        out_ktb.write(kerning_table.serialize())
