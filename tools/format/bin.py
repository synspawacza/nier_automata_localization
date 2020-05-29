#!/usr/bin/python3

from format.utils import *

# based on:
#   https://github.com/mrubyc/mrubyc/blob/master/doc/bytecode_format.md
#   https://github.com/mrubyc/mrubyc/blob/master/doc/opcodes.md
#   https://github.com/mruby/mruby/blob/master/src/load.c

# based on https://github.com/mruby/mruby/blob/master/src/crc.c
def calc_crc(bytes):
    CRC_PATTERN = 0x11021 << 8
    CARRY_BIT = 0x01000000
    work = 0
    for byte in bytes:
        work |= byte
        for i in range(8):  # each bit
            work <<= 1
            if work & CARRY_BIT:
                work ^= CRC_PATTERN
    return work >> 8


def mruby_op_string(index, pool_id):
    return (index << 23) | (pool_id << 7) | 0x3D


def mruby_opcode(value):
    return value & 0x7F


def get_bx(value):
    return (value >> 7) & 0xFFFF


OP_SETCONST = 0x12
OP_ARRAY = 0x37
OP_STRING = 0x3D


class Header:
    @staticmethod
    def parse(reader):
        result = Header()
        result.magic = read_bytes(reader, 4)
        assert_magic(result.magic, b"RITE")
        result.version = read_utf8(reader, 4)
        read_bytes(reader, 2)  # ignore crc
        result.size = read_be_int(reader, 4)
        result.compiler = read_utf8(reader, 8)
        return result

    def serialize(self):
        result = bytearray()
        result += self.magic
        result += write_utf8(self.version, 4)
        result += bytearray(b"\0" * 6)  # CRC + size to be replaced later
        result += write_utf8(self.compiler, 8)
        return result


class PoolRecord:
    @staticmethod
    def parse(reader):
        result = PoolRecord()
        result.type = read_bytes(reader, 1)
        size = read_be_int(reader, 2)
        result.value = read_utf8(reader, size)
        return result

    @staticmethod
    def from_string(value=""):
        result = PoolRecord()
        result.type = b"\0"
        result.value = value
        return result

    def serialize(self):
        result = bytearray()
        result += self.type
        content = write_utf8(self.value, len(self.value))
        result += write_be_int(len(content), 2)
        result += content
        return result


class IrepSegment:
    @staticmethod
    def parse(reader):
        result = IrepSegment()
        read_be_int(reader, 4)  # size
        result.nlocals = read_be_int(reader, 2)
        result.nregs = read_be_int(reader, 2)
        result.rlen = read_be_int(reader, 2)

        ninstructions = read_be_int(reader, 4)
        read_padding(reader, 4)
        result.instructions = []
        for i in range(ninstructions):
            result.instructions.append(read_be_int(reader, 4))

        npool = read_be_int(reader, 4)
        result.pool = []
        for i in range(npool):
            result.pool.append(PoolRecord.parse(reader))

        nsymbols = read_be_int(reader, 4)
        result.symbols = []
        for i in range(nsymbols):
            symbol_size = read_be_int(reader, 2)
            if symbol_size == 0xFFFF:
                result.symbols.append("")  # null symbol
            else:
                result.symbols.append(read_utf8(reader, symbol_size + 1))
        return result

    def serialize(self, offset):
        result = bytearray()

        result += b"\0" * 4  # size placeholder
        result += write_be_int(self.nlocals, 2)
        result += write_be_int(self.nregs, 2)
        result += write_be_int(self.rlen, 2)

        result += write_be_int(len(self.instructions), 4)

        padding = write_padding(offset + len(result), 4)
        padding_size = len(padding)
        result += padding

        for instr in self.instructions:
            result += write_be_int(instr, 4)

        result += write_be_int(len(self.pool), 4)
        for val in self.pool:
            result += val.serialize()

        result += write_be_int(len(self.symbols), 4)
        for symbol in self.symbols:
            size = len(symbol)
            if size == 0:
                result += write_be_int(0xFFFF, 2)
            else:
                result += write_be_int(size, 2)
                result += write_utf8(symbol, size + 1)

        # update reported size to match actul size (with some fiddling around padding bytes)
        result[0:4] = write_be_int(len(result) + 4 - padding_size, 4)

        return result


class IrepSection:
    @staticmethod
    def parse(reader):
        result = IrepSection()
        result.type = read_bytes(reader, 4)
        size = read_be_int(reader, 4)
        endoffset = reader.tell() + size - 8
        result.version = read_bytes(reader, 4)
        result.segments = []
        while reader.tell() < endoffset:
            result.segments.append(IrepSegment.parse(reader))
        return result

    def serialize(self, offset):
        result = bytearray()
        result += self.type
        result += bytearray(b"\0" * 4)  # size placeholder
        result += self.version
        for segment in self.segments:
            result += segment.serialize(offset + len(result))
        result[4:8] = write_be_int(len(result), 4)
        return result


class UnknownSection:
    @staticmethod
    def parse(reader):
        result = UnknownSection()
        result.type = read_bytes(reader, 4)
        size = read_be_int(reader, 4)
        result.content = read_bytes(reader, size - 8)
        return result

    def serialize(self, offset):
        result = bytearray()
        result += self.type
        result += bytearray(b"\0" * 4)  # size placeholder
        result += self.content
        result[4:8] = write_be_int(len(result), 4)
        return result


class File:
    @staticmethod
    def parse(reader):
        result = File()
        reader.seek(0)

        result.header = Header.parse(reader)
        result.sections = []

        while reader.tell() < result.header.size:
            section_type = peek_bytes(reader, 4)
            if section_type == b"IREP":
                result.sections.append(IrepSection.parse(reader))
            else:
                result.sections.append(UnknownSection.parse(reader))

        return result

    def serialize(self):
        result = bytearray()
        result += self.header.serialize()
        for section in self.sections:
            result += section.serialize(len(result))
        result[10:14] = write_be_int(len(result), 4)
        result[8:10] = write_be_int(calc_crc(result[10:]), 2)
        return result

    def get_strings(self, lang):
        result = dict()

        LANGS = {"jp": 0, "en": 1, "fr": 2, "it": 3, "de": 4, "es": 5}
        lang_index = LANGS[lang]

        for section in self.sections:
            if not isinstance(section, IrepSection):
                continue
            for segment in section.segments:
                for instr_idx, instr in enumerate(segment.instructions):
                    array_size = 0
                    if instr == 0x804437:  # OP_ARRAY 1 1 8
                        array_size = 8
                    elif instr == 0x804337:  # OP_ARRAY 1 1 6
                        array_size = 6
                    else:
                        continue

                    symbol_instr = segment.instructions[instr_idx + 1]
                    assert mruby_opcode(symbol_instr) == OP_SETCONST
                    symbol = segment.symbols[get_bx(symbol_instr)]

                    str_instr = segment.instructions[
                        instr_idx - array_size + lang_index
                    ]
                    result[symbol] = segment.pool[get_bx(str_instr)].value

        return dict(sorted(result.items()))

    def put_strings(self, mapping, lang):
        LANGS = {"jp": 0, "en": 1, "fr": 2, "it": 3, "de": 4, "es": 5}
        lang_index = LANGS[lang]

        for section in self.sections:
            if not isinstance(section, IrepSection):
                continue
            for segment in section.segments:
                for instr_idx, instr in enumerate(segment.instructions):
                    array_size = 0
                    if instr == 0x804437:  # OP_ARRAY 1 1 8
                        array_size = 8
                    elif instr == 0x804337:  # OP_ARRAY 1 1 6
                        array_size = 6
                    else:
                        continue

                    symbol_instr = segment.instructions[instr_idx + 1]
                    assert mruby_opcode(symbol_instr) == OP_SETCONST
                    symbol = segment.symbols[get_bx(symbol_instr)]

                    prev_str_instr = segment.instructions[
                        instr_idx - array_size + lang_index
                    ]
                    prev_str = segment.pool[get_bx(prev_str_instr)].value
                    if mapping[symbol] != prev_str:
                        segment.pool.append(PoolRecord.from_string(mapping[symbol]))
                        segment.instructions[
                            instr_idx - array_size + lang_index
                        ] = mruby_op_string(2, len(segment.pool) - 1)
