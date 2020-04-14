#!/usr/bin/python3

def assert_magic(magic, reference):
    l = len(reference)
    if magic[0:l] != reference:
        raise Exception("Invalid magic value in file: expected "+ reference.hex() +", was: "+magic[0:l].hex())


def read_bytes(reader, byte_count):
    return reader.read(byte_count)


def read_int(reader, byte_count):
    return int.from_bytes(reader.read(byte_count), "little", signed=True)


def write_int(value, byte_count):
    return value.to_bytes(byte_count, "little", signed=True)


def read_utf8(reader, byte_count):
    return reader.read(byte_count).decode("utf-8").rstrip("\0")


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
