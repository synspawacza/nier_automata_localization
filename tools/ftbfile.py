#!/usr/bin/python3

import os

class Header:
    HEADER_SIZE = 136
    
    def __init__(self, bytes):
        self.magic = bytes[0:118]
        self.textures_count = int.from_bytes(bytes[118:118+2], 'little')
        self.unknown = bytes[120:120+2]
        self.chars_count = int.from_bytes(bytes[122:122+2], 'little')
        self.textures_offset = int.from_bytes(bytes[124:124+4], 'little')
        self.chars_offset = int.from_bytes(bytes[128:128+4], 'little')
        self.chars_offset2 = int.from_bytes(bytes[132:132+4], 'little')

class Character:
    ENTRY_SIZE = 12
    
    def __init__(self, bytes):
        self.char = bytes[0:2].decode("utf-16-le")
        self.texture_id = int.from_bytes(bytes[2:2+2], 'little')
        self.width = int.from_bytes(bytes[4:4+2], 'little')
        self.height = int.from_bytes(bytes[6:6+2], 'little')
        self.u = int.from_bytes(bytes[8:8+2], 'little')
        self.v = int.from_bytes(bytes[10:10+2], 'little')
        
    def serialize(self):
        result = self.char.encode("utf-16-le").ljust(2, b'\0')
        result += self.texture_id.to_bytes(2, 'little')
        result += self.width.to_bytes(2, 'little')
        result += self.height.to_bytes(2, 'little')
        result += self.u.to_bytes(2, 'little')
        result += self.v.to_bytes(2, 'little')
        return result
        
class FtbFile:
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        self.header = Header(byte_reader.read(Header.HEADER_SIZE))
        
        byte_reader.seek(self.header.textures_offset)
        self.textures = byte_reader.read(self.header.textures_count*16)
        
        byte_reader.seek(self.header.chars_offset)
        self.chars = []
        for i in range(self.header.chars_count):
            self.chars.append(Character(byte_reader.read(Character.ENTRY_SIZE)))
            
    def serialize(self):
        result = self.header.magic
        result += self.header.textures_count.to_bytes(2, 'little')
        result += self.header.unknown
        result += len(self.chars).to_bytes(2, 'little')
        result += self.header.textures_offset.to_bytes(4, 'little')
        result += self.header.chars_offset.to_bytes(4, 'little')
        result += self.header.chars_offset.to_bytes(4, 'little')
        result += self.textures
        for c in self.chars:
            result += c.serialize()
        result += b'\0'*0x88 #padding?
        return result