#!/usr/bin/python3

from format.utils import *


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        count = read_int(reader, 2)

        result.entries = {}
        for i in range(count):
            left = read_utf16(reader, 2)
            right = read_utf16(reader, 2)
            kerning = read_int(reader, 2)
            result.entries[(left, right)] = kerning
        return result

    def clone_kerning(self, from_char, to_char):
        new_entries = {}
        for e in self.entries:
            if e[0] == from_char or e[1] == from_char:
                left = e[0] if e[0] != from_char else to_char
                right = e[1] if e[1] != from_char else to_char
                new_entries[(left, right)] = self.entries[e]
        self.entries = {**self.entries, **new_entries}

    def get_kerning(self, left, right):
        if (left, right) in self.entries:
            return self.entries[(left, right)]
        else:
            return 0

    def serialize(self):
        result = bytearray()
        result += write_int(len(self.entries), 2)
        for key, value in self.entries.items():
            result += write_utf16(key[0], 2)
            result += write_utf16(key[1], 2)
            result += write_int(value, 2)
        return result
