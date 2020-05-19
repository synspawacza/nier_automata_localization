#!/usr/bin/python3

from format.utils import *

# based on https://gist.github.com/Wunkolo/213aa61eb0c874172aec97ebb8ab89c2
# based on https://github.com/xxk-i/DATrepacker/blob/master/dat_utils.py


class Header:
    HEADER_SIZE = 32

    @staticmethod
    def parse(reader):
        result = Header()
        result.magic = read_bytes(reader, 4)
        assert_magic(result.magic, b"DAT\0")
        result.file_count = read_int(reader, 4)
        result.file_table_offset = read_int(reader, 4)
        result.ext_table_offset = read_int(reader, 4)
        result.name_table_offset = read_int(reader, 4)
        result.size_table_offset = read_int(reader, 4)
        result.crc_table_offset = read_int(reader, 4)
        result.unknown = read_bytes(reader, 4)
        return result

    def serialize(self):
        result = bytearray()
        result += self.magic
        result += write_int(self.file_count, 4)
        result += write_int(self.file_table_offset, 4)
        result += write_int(self.ext_table_offset, 4)
        result += write_int(self.name_table_offset, 4)
        result += write_int(self.size_table_offset, 4)
        result += write_int(self.crc_table_offset, 4)
        result += self.unknown
        return result


class Entry:
    def __init__(self):
        self.name = None
        self.offset = None
        self.size = None
        self.bytes = None


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)
        result.header = Header.parse(reader)

        result.files = [Entry() for i in range(result.header.file_count)]

        reader.seek(result.header.file_table_offset)
        for i in range(result.header.file_count):
            result.files[i].offset = read_int(reader, 4)

        reader.seek(result.header.size_table_offset)
        for i in range(result.header.file_count):
            result.files[i].size = read_int(reader, 4)

        reader.seek(result.header.name_table_offset)
        filename_len = read_int(reader, 4)
        for i in range(result.header.file_count):
            result.files[i].name = read_utf8(reader, filename_len)

        reader.seek(result.header.crc_table_offset)
        if len(result.files) > 0:
            result.crc_table = read_bytes(
                reader, result.files[0].offset - result.header.crc_table_offset
            )
        else:
            result.crc_table = b""

        for i in range(result.header.file_count):
            reader.seek(result.files[i].offset)
            result.files[i].bytes = read_bytes(reader, result.files[i].size)

        return result

    def serialize(self):
        result = bytearray(b"\0" * Header.HEADER_SIZE)  # placeholder
        self.header.file_count = len(self.files)

        self.header.file_table_offset = len(result)
        result += b"\0" * 4 * self.header.file_count  # placeholder

        self.header.ext_table_offset = len(result)
        for file in self.files:
            result += write_utf8(file.name.split(".")[-1], 4)

        self.header.name_table_offset = len(result)
        filename_len = max([len(f.name) for f in self.files]) + 1
        result += write_int(filename_len, 4)
        for file in self.files:
            result += write_utf8(file.name, filename_len)

        result += write_padding(len(result), 4)

        self.header.size_table_offset = len(result)
        for file in self.files:
            result += write_int(len(file.bytes), 4)

        self.header.crc_table_offset = len(result)
        result += self.crc_table  # keep the same CRC

        result += write_padding(len(result), 16)

        offset_table = bytearray()
        for file in self.files:
            file_offset = len(result)
            offset_table += write_int(file_offset, 4)
            result += file.bytes
            result += write_padding(len(result), 16)

        result[0 : Header.HEADER_SIZE] = self.header.serialize()
        result[
            self.header.file_table_offset : self.header.file_table_offset
            + len(offset_table)
        ] = offset_table

        return result
