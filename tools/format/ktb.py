#!/usr/bin/python3

from format.utils import *


class Entry:
    @staticmethod
    def parse(reader):
        result = Entry()
        result.left = read_utf16(reader, 2)
        result.right = read_utf16(reader, 2)
        result.kerning = read_int(reader, 2)
        return result

    def serialize(self):
        result = bytearray()
        result += write_utf16(self.left, 2)
        result += write_utf16(self.right, 2)
        result += write_int(self.kerning, 2)
        return result


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        count = read_int(reader, 2)

        result.entries = []
        for i in range(count):
            result.entries.append(Entry.parse(reader))
        return result

    def clone_kerning(self, from_char, to_char):
        new_entries = list()
        for e in self.entries:
            if e.left == from_char or e.right == from_char:
                new_entry = Entry()
                new_entry.left = e.left if e.left != from_char else to_char
                new_entry.right = e.right if e.right != from_char else to_char
                new_entry.kerning = e.kerning
                new_entries.append(new_entry)
        self.entries += new_entries

    def serialize(self):
        result = bytearray()
        result += write_int(len(self.entries), 2)
        for e in self.entries:
            result += e.serialize()
        return result
