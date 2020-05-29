#!/usr/bin/python3

from format.utils import *


class Entry:
    @staticmethod
    def parse(reader):
        result = Entry()
        idsize = read_int(reader, 4) * 2
        result.id = read_utf16(reader, idsize)
        textsize = read_int(reader, 4) * 2
        result.text = read_utf16(reader, textsize)
        return result

    def serialize(self):
        result = bytearray()
        idsize = len(self.id) + 1
        result += write_int(idsize, 4)
        result += write_utf16(self.id, idsize * 2)
        textsize = len(self.text) + 1
        result += write_int(textsize, 4)
        result += write_utf16(self.text, textsize * 2)
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
