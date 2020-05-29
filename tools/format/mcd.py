#!/usr/bin/python3

from format.utils import *

# based on https://zenhax.com/viewtopic.php?t=1502&p=8181
# based on https://github.com/Kerilk/bayonetta_tools/blob/master/binary_templates/Bayonetta%202%20mcd%20base.bt


class Header:
    ENTRY_SIZE = 40

    @staticmethod
    def parse(reader):
        result = Header()
        result.messages_offset = read_int(reader, 4)
        result.messages_count = read_int(reader, 4)
        result.symbols_offset = read_int(reader, 4)
        result.symbols_count = read_int(reader, 4)
        result.glyphs_offset = read_int(reader, 4)
        result.glyphs_count = read_int(reader, 4)  # should be the same as symbols_count
        result.fonts_offset = read_int(reader, 4)
        result.fonts_count = read_int(reader, 4)
        result.events_offset = read_int(reader, 4)
        result.events_count = read_int(reader, 4)  # should be thesame as messages_count
        return result

    def serialize(self):
        result = bytearray()
        result += write_int(self.messages_offset, 4)
        result += write_int(self.messages_count, 4)
        result += write_int(self.symbols_offset, 4)
        result += write_int(self.symbols_count, 4)
        result += write_int(self.glyphs_offset, 4)
        result += write_int(self.glyphs_count, 4)
        result += write_int(self.fonts_offset, 4)
        result += write_int(self.fonts_count, 4)
        result += write_int(self.events_offset, 4)
        result += write_int(self.events_count, 4)
        return result


class Symbol:
    # interesting anomaly: character \x80 seems to be used as ellipsis character (…)
    ENTRY_SIZE = 8

    @staticmethod
    def parse(reader):
        result = Symbol()
        result.font_id = read_int(reader, 2)
        result.char = read_utf16(reader, 2)
        result.glyph_id = read_int(reader, 4)
        return result

    def serialize(self):
        result = bytearray()
        result += write_int(self.font_id, 2)
        result += write_utf16(self.char, 2)
        result += write_int(self.glyph_id, 4)
        return result


class Glyph:
    ENTRY_SIZE = 40

    @staticmethod
    def parse(reader):
        result = Glyph()
        result.texture = read_int(reader, 4)
        result.u1 = read_float(reader)
        result.v1 = read_float(reader)
        result.u2 = read_float(reader)
        result.v2 = read_float(reader)
        result.width = read_float(reader)
        result.height = read_float(reader)  # same as font.height, sometimes diff by 1
        result.above = read_float(reader)
        result.below = read_float(reader)  # same as font.below
        result.horiz = read_float(reader)  # same as font.horiz and equal 0
        return result

    def serialize(self):
        result = bytearray()
        result += write_int(self.texture, 4)
        result += write_float(self.u1)
        result += write_float(self.v1)
        result += write_float(self.u2)
        result += write_float(self.v2)
        result += write_float(self.width)
        result += write_float(self.height)
        result += write_float(self.above)
        result += write_float(self.below)
        result += write_float(self.horiz)
        return result


class Font:
    ENTRY_SIZE = 20

    @staticmethod
    def parse(reader):
        result = Font()
        result.id = read_int(reader, 4)
        result.width = read_float(reader)
        result.height = read_float(reader)
        result.below = read_float(reader)
        result.horiz = read_float(reader)
        return result

    def serialize(self):
        result = bytearray()
        result += write_int(self.id, 4)
        result += write_float(self.width)
        result += write_float(self.height)
        result += write_float(self.below)
        result += write_float(self.horiz)
        return result


class Event:
    ENTRY_SIZE = 40

    @staticmethod
    def parse(reader):
        result = Event()
        result.id = read_int(reader, 4)
        result.idx = read_int(reader, 4)
        result.name = read_utf8(reader, 32)
        return result

    def serialize(self):
        result = bytearray()
        result += write_int(self.id, 4)
        result += write_int(self.idx, 4)
        result += write_utf8(self.name, 32)
        return result


class Message:
    ENTRY_SIZE = 16

    @staticmethod
    def parse(reader):
        result = Message()
        result.texts = []
        texts_offset = read_int(reader, 4)
        texts_count = read_int(reader, 4)
        result.seq_number = read_int(reader, 4)
        result.event_id = read_int(reader, 4)

        last_pos = reader.tell()
        reader.seek(texts_offset)
        for i in range(texts_count):
            result.texts.append(Text.parse(reader))
        reader.seek(last_pos)

        return result

    def serialize(self, texts_offset):
        result = bytearray()
        result += write_int(texts_offset, 4)
        result += write_int(len(self.texts), 4)
        result += write_int(self.seq_number, 4)
        result += write_int(self.event_id, 4)
        return result

    def as_string(self, symbols):
        # using first text - other texts have the same content, but using different font
        return self.texts[0].as_string(symbols)

    def put_string(self, value, symbols, fonts):
        for text in self.texts:
            text.put_string(value, symbols, fonts)


class Text:
    ENTRY_SIZE = 20

    @staticmethod
    def parse(reader):
        result = Text()
        result.lines = []
        lines_offset = read_int(reader, 4)
        lines_count = read_int(reader, 4)
        result.vpos = read_int(reader, 4)
        result.hpos = read_int(reader, 4)
        result.font = read_int(reader, 4)  # ???? it is font ?

        last_pos = reader.tell()
        reader.seek(lines_offset)
        for i in range(lines_count):
            result.lines.append(Line.parse(reader))
        reader.seek(last_pos)

        return result

    def serialize(self, lines_offset):
        result = bytearray()
        result += write_int(lines_offset, 4)
        result += write_int(len(self.lines), 4)
        result += write_int(self.vpos, 4)
        result += write_int(self.hpos, 4)
        result += write_int(self.font, 4)
        return result

    def as_string(self, symbols):
        return "\n".join([line.as_string(symbols) for line in self.lines])

    def put_string(self, value, symbols, fonts):
        font = fonts[self.font]
        self.lines = [
            Line.from_string(line, font, symbols) for line in value.split("\n")
        ]


class Line:
    ENTRY_SIZE = 24

    @staticmethod
    def from_string(value, font, symbols):
        result = Line()
        result.content = []
        result.padding = 0
        result.below = font.line_below_value()
        result.horiz = 0
        result.put_string(value, symbols, font)
        return result

    @staticmethod
    def parse(reader):
        result = Line()
        result.content = []
        content_offset = read_int(reader, 4)
        result.padding = read_int(reader, 4)
        content_length = read_int(reader, 4)
        read_int(reader, 4)  # skip length2
        result.below = read_float(reader)
        result.horiz = read_float(reader)

        last_pos = reader.tell()
        reader.seek(content_offset)
        for i in range(content_length):
            val = read_int(reader, 2)
            if val < -32000:
                val = val & 0xFFFF
            result.content.append(val)
        reader.seek(last_pos)

        return result

    def serialize(self, content_offset):
        result = bytearray()
        result += write_int(content_offset, 4)
        result += write_int(self.padding, 4)
        result += write_int(len(self.content), 4)
        result += write_int(len(self.content), 4)
        result += write_float(self.below)
        result += write_float(self.horiz)
        return result

    def as_string(self, symbols):
        result = ""
        idx = 0
        while idx < len(self.content):
            char_id = self.content[idx]
            if char_id < 0x8000:
                result += symbols[char_id].char
                idx += 2  # skip kerning
            elif char_id == 0x8001:
                result += " "
                idx += 2  # skip font id
            elif char_id == 0x8000:
                # text end
                idx += 1
            elif char_id == 0x8020:
                result += "<special:" + str(self.content[idx + 1]) + ">"
                idx += 2
            else:
                # using '<' and '>' for tagging - hopefully it doesn't break anything
                result += "<unknown:" + str(char_id)
                if idx + 1 < len(self.content):
                    result += ":" + str(self.content[idx + 1])
                result += ">"
                idx += 2  # skip kerning
        return result

    def put_string(self, value, symbols, font):
        i = 0
        while i < len(value):
            if value.startswith("<special:", i):
                i1 = value.find(":", i) + 1
                i2 = value.find(">", i)
                self.content.append(0x8020)
                self.content.append(int(value[i1:i2]))
                i = i2
            elif value[i] == " ":
                self.content.append(0x8001)
                self.content.append(font.id)
            else:
                char_id = -1
                for id, symbol in enumerate(symbols):
                    if symbol.font_id == font.id and symbol.char == value[i]:
                        char_id = id
                if char_id < 0:
                    raise Exception(
                        "No glyph for '" + value[i] + "' in font " + font.id
                    )
                self.content.append(char_id)
                if i > 0:
                    self.content.append(font.get_kerning(value[i - 1], value[i]))
                else:
                    self.content.append(0)
            i += 1
        self.content.append(0x8000)


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        result.header = Header.parse(reader)

        reader.seek(result.header.messages_offset)
        result.messages = []
        for i in range(result.header.messages_count):
            result.messages.append(Message.parse(reader))

        reader.seek(result.header.symbols_offset)
        result.symbols = []
        for i in range(result.header.symbols_count):
            result.symbols.append(Symbol.parse(reader))

        reader.seek(result.header.glyphs_offset)
        result.glyphs = []
        for i in range(result.header.glyphs_count):
            result.glyphs.append(Glyph.parse(reader))

        reader.seek(result.header.fonts_offset)
        result.fonts = []
        for i in range(result.header.fonts_count):
            result.fonts.append(Font.parse(reader))

        reader.seek(result.header.events_offset)
        result.events = []
        for i in range(result.header.events_count):
            result.events.append(Event.parse(reader))
        return result

    def serialize(self):
        result = bytearray()

        current_offset = Header.ENTRY_SIZE

        strings = []
        strings_offsets = []

        texts = []
        texts_offsets = []

        lines = []
        lines_offsets = []

        for message in self.messages:
            for text in message.texts:
                texts.append(text)
                for line in text.lines:
                    strings.append(line.content)
                    strings_offsets.append(current_offset)
                    current_offset += len(line.content) * 2
                    lines.append(line)
        current_offset += calc_eager_padding(current_offset, 4)

        header = Header()
        header.messages_offset = current_offset
        header.messages_count = len(self.messages)
        current_offset += header.messages_count * Message.ENTRY_SIZE
        current_offset += calc_eager_padding(current_offset, 4)

        for i in range(len(texts)):
            texts_offsets.append(current_offset + i * Text.ENTRY_SIZE)
        current_offset += len(texts) * Text.ENTRY_SIZE
        current_offset += calc_eager_padding(current_offset, 4)

        for i in range(len(lines)):
            lines_offsets.append(current_offset + i * Line.ENTRY_SIZE)
        current_offset += len(lines) * Line.ENTRY_SIZE
        current_offset += calc_eager_padding(current_offset, 4)

        header.symbols_offset = current_offset
        header.symbols_count = len(self.symbols)
        current_offset += header.symbols_count * Symbol.ENTRY_SIZE + 4

        header.glyphs_offset = current_offset
        header.glyphs_count = len(self.glyphs)
        current_offset += header.glyphs_count * Glyph.ENTRY_SIZE + 4

        header.fonts_offset = current_offset
        header.fonts_count = len(self.fonts)
        current_offset += header.fonts_count * Font.ENTRY_SIZE + 4

        header.events_offset = current_offset
        header.events_count = len(self.events)

        result += header.serialize()
        for string in strings:
            for v in string:
                result += write_int(v, 2)
        result += write_eager_padding(len(result), 4)

        texts_offset_idx = 0
        for message in self.messages:
            texts_offset = texts_offsets[texts_offset_idx]
            texts_offset_idx += len(message.texts)
            result += message.serialize(texts_offset)
        result += write_eager_padding(len(result), 4)

        lines_offset_idx = 0
        for text in texts:
            lines_offset = lines_offsets[lines_offset_idx]
            lines_offset_idx += len(text.lines)
            result += text.serialize(lines_offset)
        result += write_eager_padding(len(result), 4)

        strings_idx = 0
        for line in lines:
            strings_offset = strings_offsets[strings_idx]
            strings_idx += 1
            result += line.serialize(strings_offset)
        result += write_eager_padding(len(result), 4)

        for symbol in self.symbols:
            result += symbol.serialize()
        result += write_eager_padding(len(result), 4)

        for glyph in self.glyphs:
            result += glyph.serialize()
        result += write_eager_padding(len(result), 4)

        for font in self.fonts:
            result += font.serialize()
        result += write_eager_padding(len(result), 4)

        for event in self.events:
            result += event.serialize()

        return result

    def get_strings(self, lang):
        result = dict()
        for msg in self.messages:
            matching_events = list(filter(lambda e: e.id == msg.event_id, self.events))
            assert len(matching_events) == 1
            event = matching_events[0].name
            result[event] = msg.as_string(self.symbols)
        return result

    def get_fonts_for_messages(self):
        result = dict()
        for msg in self.messages:
            matching_events = list(filter(lambda e: e.id == msg.event_id, self.events))
            assert len(matching_events) == 1
            event = matching_events[0].name
            result[event] = set()
            for text in msg.texts:
                result[event].add(text.font)
        return result

    def get_glyphs(self, textures, font_id):
        result = {}
        for symbol in self.symbols:
            if symbol.font_id != font_id:
                continue
            glyph = self.glyphs[symbol.glyph_id]
            texture = textures[0]
            u1 = glyph.u1 * texture.width
            u2 = glyph.u2 * texture.width
            v1 = glyph.v1 * texture.height
            v2 = glyph.v2 * texture.height
            result[symbol.char] = texture.crop((u1, v1, u2, v2))
        return result

    def remove_all_glyphs(self):
        self.symbols = []
        self.glyphs = []
        pass

    def put_glyph(
        self, char, font_id, x, y, width, height, texture_width, texture_height
    ):
        glyph = Glyph()
        glyph.texture = 0
        glyph.u1 = x / texture_width
        glyph.v1 = y / texture_height
        glyph.u2 = (x + width) / texture_width
        glyph.v2 = (y + height) / texture_height
        glyph.width = width
        glyph.height = height
        glyph.above = 0
        font = next(f for f in self.fonts if f.id == font_id)
        glyph.below = font.below
        glyph.horiz = font.horiz
        self.glyphs.append(glyph)

        symbol = Symbol()
        symbol.font_id = font_id
        symbol.char = char
        symbol.glyph_id = len(self.glyphs) - 1
        self.symbols.append(symbol)
        pass

    def put_strings(self, mapping, fonts):
        for msg in self.messages:
            matching_events = list(filter(lambda e: e.id == msg.event_id, self.events))
            assert len(matching_events) == 1
            event = matching_events[0].name
            value = mapping[event]
            msg.put_string(value, self.symbols, fonts)
