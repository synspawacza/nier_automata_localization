#!/usr/bin/python3

from format.utils import *
import os


class Header:
    HEADER_SIZE = 32

    @staticmethod
    def parse(reader):
        result = Header()
        result.magic = read_bytes(reader, 8)
        assert_magic(result.magic, b"WTB\0")
        result.textures_count = read_int(reader, 4)
        result.offsets_offset = read_int(reader, 4)
        result.size_offset = read_int(reader, 4)
        result.flags_offset = read_int(reader, 4)
        result.idx_offset = read_int(reader, 4)
        result.info_offset = read_int(reader, 4)
        return result

    def serialize(self):
        result = bytearray()
        result += self.magic
        result += write_int(self.textures_count, 4)
        result += write_int(self.offsets_offset, 4)
        result += write_int(self.size_offset, 4)
        result += write_int(self.flags_offset, 4)
        result += write_int(self.idx_offset, 4)
        result += write_int(self.info_offset, 4)
        return result


class Entry:
    def __init__(self):
        self.idx = None
        self.offset = None
        self.size = None
        self.flags = None
        self.info = None

    def is_astc(self):
        if not self.info:
            return False
        return self.info[4] in {0x79, 0x7D, 0x8B}

    def tex_width(self):
        return int.from_bytes(self.info[12:15], "little", signed=False)

    def tex_height(self):
        return int.from_bytes(self.info[16:19], "little", signed=False)

    def astc_header(self):
        return (
            b"\x13\xAB\xA1\x5C\x06\x06\0"
            + self.info[12:15]
            + self.info[16:19]
            + b"\1\0\0"
        )


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        result.header = Header.parse(reader)

        result.textures = [Entry() for i in range(result.header.textures_count)]

        reader.seek(result.header.offsets_offset)
        for i in range(result.header.textures_count):
            result.textures[i].offset = read_int(reader, 4)

        reader.seek(result.header.size_offset)
        for i in range(result.header.textures_count):
            result.textures[i].size = read_int(reader, 4)

        reader.seek(result.header.flags_offset)
        for i in range(result.header.textures_count):
            result.textures[i].flags = read_bytes(reader, 4)

        reader.seek(result.header.idx_offset)
        for i in range(result.header.textures_count):
            result.textures[i].idx = read_bytes(reader, 4)

        result.has_info_table = result.header.info_offset > 0
        if result.has_info_table:
            reader.seek(0, os.SEEK_END)
            end_pos = reader.tell()
            info_record_size = int(
                (end_pos - result.header.info_offset) / result.header.textures_count
            )
            if info_record_size < 256 and info_record_size > 0:
                info_record_size = 20
            reader.seek(result.header.info_offset)
            for i in range(result.header.textures_count):
                result.textures[i].info = read_bytes(reader, info_record_size)

        return result

    def serialize(self):
        result = bytearray(b"\0" * Header.HEADER_SIZE)  # placeholder
        self.header.textures_count = len(self.textures)

        self.header.offsets_offset = len(result)
        texture_offset = 0
        TEXTURE_OFFSET_PADDING = 0x1000
        for texture in self.textures:
            result += write_int(texture_offset, 4)
            texture_offset += texture.size
            texture_offset += (
                TEXTURE_OFFSET_PADDING - texture_offset % TEXTURE_OFFSET_PADDING
            ) % TEXTURE_OFFSET_PADDING
        result += write_padding(len(result), 32)

        self.header.size_offset = len(result)
        for texture in self.textures:
            result += write_int(texture.size, 4)
        result += write_padding(len(result), 32)

        self.header.flags_offset = len(result)
        for texture in self.textures:
            result += texture.flags
        result += write_padding(len(result), 32)

        self.header.idx_offset = len(result)
        for texture in self.textures:
            result += texture.idx
        if self.has_info_table:
            result += write_padding(len(result), 32)
        else:
            result += write_padding(len(result), 16)

        if self.has_info_table:
            self.header.info_offset = len(result)
            for texture in self.textures:
                result += texture.info
            result += write_padding(len(result), 16)
        else:
            self.header.info_offset = 0

        result[0 : Header.HEADER_SIZE] = self.header.serialize()

        return result
