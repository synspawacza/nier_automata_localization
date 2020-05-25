#!/usr/bin/python3

import argparse
import format.ftb as ftb
from PIL import Image


def add_glyphs(font, texture, page, chars):
    for char, glyph in chars:
        x, y = font.find_space_for_glyph(glyph.size, texture.size, page)
        font.add_character(char, page, glyph.width, glyph.height, x, y)
        texture.paste(glyph, (x, y))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_ftb", help="source font file")
    parser.add_argument("input_texture", help="source texture file (can be .dds)")
    parser.add_argument("output_ftb", help="target font file")
    parser.add_argument(
        "output_texture",
        help="target texture file (cannot be .dds, but .png can be used)",
    )
    parser.add_argument(
        "--page", help="texture number", required=True, type=int,
    )
    parser.add_argument(
        "--char",
        help="character id and glyph image",
        metavar=("CHARID", "CHARIMG"),
        nargs=2,
        action="append",
    )

    args = parser.parse_args()

    font = None
    with open(args.input_ftb, "rb") as input_ftb:
        font = ftb.File.parse(input_ftb)
    texture = Image.open(args.input_texture)

    chars = [(chr(int(c)), Image.open(tex)) for c, tex in args.char]

    add_glyphs(font, texture, args.page, chars)

    with open(args.output_ftb, "wb") as out_ftb:
        out_ftb.write(font.serialize())
    texture.save(args.output_texture)
