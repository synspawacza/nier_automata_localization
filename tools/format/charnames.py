#!/usr/bin/python3

from format.utils import *
import math


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        count = read_int(reader, 4)

        offsets = []
        for i in range(count):
            id = read_uint(reader, 5)
            offset = read_int(reader, 4)
            offsets.append((id, offset))

        result.entries = {}
        for id, offset in offsets:
            if id not in result.entries:
                result.entries[id] = ""
            if offset == 0:
                continue
            reader.seek(offset)
            result.entries[id] += read_zero_terminated_utf8(reader)

        return result

    def serialize(self):
        strings = []
        for id, value in self.entries.items():
            if value == "":
                strings.append((id, b""))
            else:
                bytes = write_utf8(value, 0)
                for i in range(math.ceil(len(bytes) / 64)):
                    strings.append((id, bytes[i * 64 : (i + 1) * 64] + b"\0"))

        result = bytearray()
        result += write_int(len(strings), 4)
        offset = 4 + 9 * len(strings)
        for id, value in strings:
            result += write_int(id, 5)
            if value == b"":
                result += write_int(0, 4)
            else:
                result += write_int(offset, 4)
            offset += len(value)
        for id, value in strings:
            result += value
        return result

    def get_strings(self, lang):
        result = dict()

        LANGS = {
            "jp": "JPN",
            "en": "ENG",
            "fr": "FRA",
            "it": "ITA",
            "de": "GER",
            "es": "ESP",
        }
        lang_id = LANGS[lang]

        character_names_table = bytes.fromhex(self.entries[0x1D77583401])[20:].decode(
            "utf-8"
        )
        for line in character_names_table.split("\n"):
            if len(line) <= 2:
                pass
            elif line[1] != " ":
                id = line.strip(" ")
            elif line[2:5] == lang_id:
                result[id] = line[6:]
        return result

    def put_strings(self, lang, mapping):
        LANGS = {
            "jp": "JPN",
            "en": "ENG",
            "fr": "FRA",
            "it": "ITA",
            "de": "GER",
            "es": "ESP",
        }
        lang_id = LANGS[lang]

        character_names_table = bytes.fromhex(self.entries[0x1D77583401])[20:].decode(
            "utf-8"
        )
        new_lines = []
        for line in character_names_table.split("\n"):
            if len(line) <= 2:
                pass
            elif line[1] != " ":
                id = line.strip(" ")
            elif line[2:5] == lang_id:
                line = line[:6] + mapping[id]
            new_lines.append(line)
        new_string = "\n".join(new_lines).encode("utf-8").hex()

        self.entries[0x1D77583401] = self.entries[0x1D77583401][:40] + new_string
        strlen = len(self.entries[0x1D77583401]) // 2
        self.entries[0xF7C0246A01] = "{:#x}".format(strlen)
