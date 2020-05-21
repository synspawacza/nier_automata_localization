#!/usr/bin/python3

import struct


def assert_magic(magic, reference):
    l = len(reference)
    if magic[0:l] != reference:
        raise Exception(
            "Invalid magic value in file: expected "
            + reference.hex()
            + ", was: "
            + magic[0:l].hex()
        )


def read_bytes(reader, byte_count):
    return reader.read(byte_count)


def peek_bytes(reader, byte_count):
    pos = reader.tell()
    bytes = reader.read(byte_count)
    reader.seek(pos)
    return bytes


def read_int(reader, byte_count):
    return int.from_bytes(reader.read(byte_count), "little", signed=True)


def read_uint(reader, byte_count):
    return int.from_bytes(reader.read(byte_count), "little", signed=False)


def write_int(value, byte_count):
    if value < 0:
        return value.to_bytes(byte_count, "little", signed=True)
    else:
        return value.to_bytes(byte_count, "little", signed=False)


def read_be_int(reader, byte_count):  # big endian
    return int.from_bytes(reader.read(byte_count), "big", signed=True)


def write_be_int(value, byte_count):  # big endian
    if value < 0:
        return value.to_bytes(byte_count, "big", signed=True)
    else:
        return value.to_bytes(byte_count, "big", signed=False)


def read_float(reader):
    return struct.unpack("f", reader.read(4))[0]


def write_float(value):
    return struct.pack("f", value)


def read_utf8(reader, byte_count):
    return reader.read(byte_count).decode("utf-8").rstrip("\0")


def read_zero_terminated_utf8(reader):
    init_offset = reader.tell()
    while reader.read(1) not in {b"\0", b""}:
        pass
    byte_count = reader.tell() - init_offset
    reader.seek(init_offset)
    return read_utf8(reader, byte_count)


def write_utf8(value, byte_count):
    return value.encode("utf-8").ljust(byte_count, b"\0")


def read_utf16(reader, byte_count):
    return reader.read(byte_count).decode("utf-16-le").rstrip("\0")


def write_utf16(value, byte_count):
    return value.encode("utf-16-le").ljust(byte_count, b"\0")


def read_padding(reader, mod):
    offset = reader.tell()
    padding_size = mod - (offset % mod)
    if padding_size != mod:
        return reader.read(padding_size)
    else:
        return b""


def write_padding(offset, mod):
    padding_size = mod - (offset % mod)
    if padding_size != mod:
        return b"\0" * padding_size
    else:
        return b""


def calc_eager_padding(offset, mod):
    return mod - (offset % mod)


def write_eager_padding(offset, mod):
    return b"\0" * calc_eager_padding(offset, mod)
