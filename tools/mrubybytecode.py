#!/usr/bin/python3

#based on:
#   https://github.com/mrubyc/mrubyc/blob/master/doc/bytecode_format.md
#   https://github.com/mrubyc/mrubyc/blob/master/doc/opcodes.md
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
    
def mruby_op_string(index, pool_id):
    return (index << 23) | (pool_id << 7) | 0x3D

class MrubyHeader:
    HEADER_SIZE = 22
    
    def __init__(self, bytes):
        self.magic = bytes[0:4]
        self.version = bytes[4:4+4]
        self.size = int.from_bytes(bytes[10:10+4], 'big')
        self.compiler = bytes[14:14+8]
    def serialize(self):
        result = self.magic
        result += self.version
        result += b'\0'*6 #CRC + size to be replaced later
        result += self.compiler
        return result

class PoolRecord:
    def __init__(self, reader):
        self.type = reader.read(1)
        size = int.from_bytes(reader.read(2), 'big') #implied by len of the array
        self.value = reader.read(size).decode("utf-8")
    
    @staticmethod
    def from_string(value=""):
        bytes = value.encode("utf-8")
        return PoolRecord(io.BytesIO(b'\0' + len(bytes).to_bytes(2, 'big') + bytes))
    
    def serialize(self):
        bytes = self.value.encode("utf-8")
        return self.type + len(bytes).to_bytes(2, 'big') + bytes

class IrepSegment:
    def __init__(self, reader, offset):
        self.size = int.from_bytes(reader.read(4), 'big') #implied by len of the array + additional calc
        self.nlocals = int.from_bytes(reader.read(2), 'big')
        self.nregs = int.from_bytes(reader.read(2), 'big')
        self.rlen = int.from_bytes(reader.read(2), 'big')
        
        ninstructions = int.from_bytes(reader.read(4), 'big') #implied by len of the array
        reader.read((4-(offset+reader.tell())) % 4) #padding - implied by position in file
        self.instructions = list()
        for i in range(ninstructions):
            self.instructions.append(int.from_bytes(reader.read(4), 'big'))
            
        npool = int.from_bytes(reader.read(4), 'big') #implied by len of the array
        self.pool = list()
        for i in range(npool):
            self.pool.append(PoolRecord(reader))
            
        nsymbols = int.from_bytes(reader.read(4), 'big') #implied by len of the array
        self.symbols = list()
        for i in range(nsymbols):
            symbol_size = int.from_bytes(reader.read(2), 'big') #implied by len of the array
            if(symbol_size == 0xFFFF):
                self.symbols.append('') #null symbol
            else:
                self.symbols.append(reader.read(symbol_size).decode("utf-8"))
                reader.read(1) # always 0x00
        
    def serialize(self, offset = 0):
        result = bytearray(self.size.to_bytes(4, 'big'))
        result += self.nlocals.to_bytes(2, 'big')
        result += self.nregs.to_bytes(2, 'big')
        result += self.rlen.to_bytes(2, 'big')
        
        result += len(self.instructions).to_bytes(4, 'big')
        
        offset += len(result)
        padding_bytes_required = (4 - (offset % 4)) % 4
        result += padding_bytes_required * b'\0'
        
        for instr in self.instructions:
            result += instr.to_bytes(4, 'big')
            
        result += len(self.pool).to_bytes(4, 'big')
        for val in self.pool:
            result += val.serialize()
            
        result += len(self.symbols).to_bytes(4, 'big')
        for symbol in self.symbols:
            if len(symbol) == 0:
                result += (0xFFFF).to_bytes(2, 'big')
            else:
                result += len(symbol).to_bytes(2, 'big')
                result += symbol.encode("utf-8")
                result += b'\0'
        
        #update reported size, because it does not match actul size
        result[0:4] = (len(result)+4-padding_bytes_required).to_bytes(4, 'big')
        
        return result

class IrepSection:
    def __init__(self, type, content, offset):
        self.magic = type
        self.version = content[0:4]
        self.segments = list()
        reader = io.BytesIO(content[4:])
        
        while reader.tell() < len(content)-4:
            self.segments.append(IrepSegment(reader, offset))
            
    def serialize(self, offset = 0):
        content =  self.version
        for segment in self.segments:
            content += segment.serialize(offset+8+len(content))
        return self.magic + (len(content)+8).to_bytes(4, 'big') + content
        
class UnknownSection:
    def __init__(self, type, size, content):
        self.bytes = type + size.to_bytes(4, 'big') + content
        
    def serialize(self, offset):
        return self.bytes

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
                section = IrepSection(section_type, section_content, section_offset)
            else:
                section = UnknownSection(section_type, section_size, section_content)
                
            
            self.sections.append(section)
        
    def serialize(self):
        result = bytearray(self.header.serialize())
        for section in self.sections:
            result += section.serialize(len(result))
        result[10:14] = len(result).to_bytes(4, 'big')
        result[8:10] = calc_crc(result[10:]).to_bytes(2, 'big')
        return result