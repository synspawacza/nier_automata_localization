#!/usr/bin/python3

from format.utils import *


class Entry:
    @staticmethod
    def parse(reader):
        result = Entry()
        result.id = read_utf16(reader, 0x80)
        result.number = read_int(reader, 8)
        result.text = read_utf16(reader, 0x800)
        return result

    def serialize(self):
        result = bytearray()
        result += write_utf16(self.id, 0x80)
        result += write_int(self.number, 8)
        result += write_utf16(self.text, 0x800)
        return result


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        count = read_int(reader, 4)

        result.entries = []
        for i in range(count):
            result.entries.append(Entry.parse(reader))

        return result

    def serialize(self):
        result = bytearray()
        result += write_int(len(self.entries), 4)
        for e in self.entries:
            result += e.serialize()
        return result

    def get_strings(self, lang):
        result = dict()
        for e in self.entries:
            result[e.id] = e.text
        return result

    def put_strings(self, mapping, lang):
        for e in self.entries:
            e.text = mapping[e.id]
