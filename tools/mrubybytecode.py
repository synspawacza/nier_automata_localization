#!/usr/bin/python3

#based on:
#   https://github.com/mrubyc/mrubyc/blob/master/doc/bytecode_format.md
#   https://github.com/mruby/mruby/blob/master/src/load.c

import os
import io

#based on https://github.com/mruby/mruby/blob/master/src/crc.c
def calc_crc(bytes):
    CRC_PATTERN = 0x11021 << 8
    CARRY_BIT = 0x01000000
    work = 0
    for byte in bytes:
        work |= byte
        for i in range(8): #each bit
            work <<= 1
            if work & CARRY_BIT:
                work ^= CRC_PATTERN
    return work >> 8

class MrubyHeader:
    HEADER_SIZE = 22
    
    def __init__(self, bytes):
        self.magic = bytes[0:4]
        self.version = bytes[4:4+4]
        self.crc = int.from_bytes(bytes[8:8+2], 'big')
        self.size = int.from_bytes(bytes[10:10+4], 'big')
        self.compiler = bytes[14:14+8]

class PoolRecord:
    def __init__(self, reader):
        self.type = reader.read(1)
        self.size = int.from_bytes(reader.read(2), 'big')
        self.value = reader.read(self.size).decode("utf-8")
        print(hex(self.type[0]) + "# " + repr(self.value))

class IrepSegment:
    def __init__(self, reader, offset):
        self.size = int.from_bytes(reader.read(4), 'big')
        self.nlocals = int.from_bytes(reader.read(2), 'big')
        self.nregs = int.from_bytes(reader.read(2), 'big')
        self.rlen = int.from_bytes(reader.read(2), 'big')
        
        self.ilen = int.from_bytes(reader.read(4), 'big')
        self.instructions_padding = reader.read((4-(offset+reader.tell())) % 4)
        self.instructions = list()
        for i in range(self.ilen):
            self.instructions.append(reader.read(4))
            
        self.npool = int.from_bytes(reader.read(4), 'big')
        self.pool = list()
        for i in range(self.npool):
            self.pool.append(PoolRecord(reader))
            
        self.nsymbols = int.from_bytes(reader.read(4), 'big')
        self.symbols = list()
        for i in range(self.nsymbols):
            symbol_size = int.from_bytes(reader.read(2), 'big')
            self.symbols.append(symbol_size.to_bytes(2, 'big') + reader.read(symbol_size+1))
        

class IrepSection:
    def __init__(self, type, size, content,  offset):
        self.magic = type
        self.size = size
        self.version = content[0:4]
        self.segments = list()
        reader = io.BytesIO(content[4:])
        
        while reader.tell() < len(content)-4:
            self.segments.append(IrepSegment(reader, offset))
        
class UnknownSection:
    def __init__(self, type, size, content):
        self.bytes = type + size.to_bytes(2, 'big') + content

class MrubyFile:    
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        self.header = MrubyHeader(byte_reader.read(MrubyHeader.HEADER_SIZE))
        self.sections = list()
        while byte_reader.tell() < self.header.size:
            section_offset = byte_reader.tell()
            section_type = byte_reader.read(4)
            section_size = int.from_bytes(byte_reader.read(4), 'big')
            section_content = byte_reader.read(section_size - 8)
            
            section = None
            if section_type == b"IREP":
                section = IrepSection(section_type, section_size, section_content, section_offset)
            else:
                section = UnknownSection(section_type, section_size, section_content)
                
            
            self.sections.append(section)