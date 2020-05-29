#!/usr/bin/python3

import argparse
import os
import json
import re
from PIL import Image

import format.mcd as mcd
import format.ktb as ktb
import format.properties as properties


class Font:
    def __init__(self, id, font_json):
        self.id = id
        self.glyphs_dir = font_json["glyphs"]
        self.kerning_table = None
        if font_json["kerning"]:
            with open(font_json["kerning"], "rb") as input_ktb:
                self.kerning_table = ktb.File.parse(input_ktb)
        self.below_value = font_json["below"]

    def get_glyph_filename(self, char):
        return os.path.join(self.glyphs_dir, "{0:04x}.png".format(ord(char)))

    def get_kerning(self, left, right):
        if not self.kerning_table:
            return 0
        else:
            return self.kerning_table.get_kerning(left, right)

    def line_below_value(self):
        return self.below_value


def build_fonts(json_filename):
    raw_fonts = None
    with open(json_filename, "rb") as json_file:
        raw_fonts = json.load(json_file)
    result = {}
    for id, font_json in raw_fonts.items():
        result[int(id)] = Font(int(id), font_json)
    return result


def get_glyphs(parsed_mcd, mapping, fonts):
    chars_per_font = {id: set() for id in fonts.keys()}
    for event, fonts_ids in parsed_mcd.get_fonts_for_messages().items():
        chars = set()
        # strip spaces and special chars
        for char in re.sub("\n| |<special:[0-9]+>", "", mapping[event]):
            chars.add(char)
        for font_id in fonts_ids:
            chars_per_font[font_id] |= chars
    result = []
    for font_id, chars in chars_per_font.items():
        for char in chars:
            result.append((char, font_id, fonts[font_id].get_glyph_filename(char)))
    return result


def generate_texture(glyphs, parsed_mcd):
    glyph_filenames = {cfi[2] for cfi in glyphs}
    glyph_images = [(Image.open(n), n) for n in glyph_filenames]
    glyph_images.sort(key=lambda elem: elem[1])  # to make deterministic
    glyph_images.sort(key=lambda elem: elem[0].width, reverse=True)
    glyph_images.sort(key=lambda elem: elem[0].height, reverse=True)

    def page_generator():
        # (x,y,w,h)
        size = 256
        yield (0, 0, size, size)
        while True:
            yield (0, size, size, size * 2)
            yield (size, 0, size * 2, size * 2)
            size *= 2

    pages = page_generator()
    x_zero = y_zero = width = height = 0
    x = 1
    y = 1
    next_row = 0
    img_positions = {}
    for img, name in glyph_images:
        if x + img.width > width:
            x = x_zero
            y = next_row
        if y + img.height > height:
            x_zero, y_zero, width, height = next(pages)
            x = x_zero
            y = y_zero
            next_row = y + 1
        img_positions[name] = (x, y)
        x += img.width
        next_row = max(next_row, y + img.height)

    texture = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for image, name in glyph_images:
        texture.paste(image, img_positions[name])

    glyph_images_map = {name: image for image, name in glyph_images}
    for char, font_id, name in glyphs:
        x, y = img_positions[name]
        char_width, char_height = glyph_images_map[name].size
        parsed_mcd.put_glyph(
            char, font_id, x, y, char_width, char_height, width, height
        )

    return texture


def insert_strings_to_file(mcd, properties):

    parsed_mcd.put_strings(mapping, lang, fonts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="source .mcd file name")
    parser.add_argument("strings", help="strings file name (*.properties)")
    parser.add_argument("fonts", help="fonts.json config file")
    parser.add_argument("output", help="target .mcd file name")
    parser.add_argument("texture", help="target .png texture file")

    args = parser.parse_args()

    parsed_mcd = None
    with open(args.input, "rb") as in_file:
        parsed_mcd = mcd.File.parse(in_file)

    mapping = None
    with open(args.strings, "rb") as properties_file:
        mapping = properties.parse_properties(properties_file)

    fonts = build_fonts(args.fonts)

    glyphs = get_glyphs(parsed_mcd, mapping, fonts)
    parsed_mcd.remove_all_glyphs()
    texture = generate_texture(glyphs, parsed_mcd)

    parsed_mcd.put_strings(mapping, fonts)

    with open(args.output, "wb") as out_file:
        out_file.write(parsed_mcd.serialize())
    texture.save(args.texture)
