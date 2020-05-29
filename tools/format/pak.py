#!/usr/bin/python3

from format.utils import *
import format.charnames as charnames
import zlib
from io import BytesIO


class Segment:
    def parse(reader, entry):
        result = Segment()
        result.entry = entry
        result.content = read_bytes(reader, entry.real_size)
        return result

    def unzip(self):
        return zlib.decompress(self.content[4:])

    def zip_and_put_data(self, data):
        zipped_bytes = zlib.compress(data, 1)
        self.entry.compressed_size = len(data)
        self.content = bytearray()
        self.content += write_int(len(zipped_bytes), 4)
        self.content += zipped_bytes
        self.content += write_padding(len(self.content), 4)

    def serialize(self):
        return self.content


class SegmentEntry:
    def parse(reader):
        result = SegmentEntry()
        result.type = read_int(reader, 4)
        if result.type == 0:
            return None
        result.compressed_size = read_int(reader, 4)
        result.offset = read_int(reader, 4)
        result.real_size = -1
        return result

    def serialize(self):
        result = bytearray()
        result += write_int(self.type, 4)
        result += write_int(self.compressed_size, 4)
        result += write_int(self.offset, 4)
        return result


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        entries = []
        entry = SegmentEntry.parse(reader)
        while entry != None:
            entries.append(entry)
            entry = SegmentEntry.parse(reader)
            pass

        offsets = [e.offset for e in entries]
        real_sizes = [o2 - o1 for o1, o2 in zip(offsets[0:], offsets[1:])]
        for entry, real_size in zip(entries, real_sizes):
            entry.real_size = real_size

        result.segments = []
        for entry in entries:
            reader.seek(entry.offset)
            result.segments.append(Segment.parse(reader, entry))
        return result

    def serialize(self):
        result = bytearray()
        offset = 12 * len(self.segments) + 4
        for segment in self.segments:
            segment.entry.offset = offset
            offset += len(segment.content)

        for segment in self.segments:
            result += segment.entry.serialize()
        result += write_int(0, 4)

        for segment in self.segments:
            result += segment.serialize()
        return result

    def get_strings(self, lang):
        return charnames.File.parse(BytesIO(self.segments[25].unzip())).get_strings(
            lang
        )

    def put_strings(self, mapping, lang):
        parsedcharnames = charnames.File.parse(BytesIO(self.segments[25].unzip()))
        parsedcharnames.put_strings(lang, mapping)
        self.segments[25].zip_and_put_data(parsedcharnames.serialize())
