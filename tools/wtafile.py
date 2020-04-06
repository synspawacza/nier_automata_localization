#!/usr/bin/python3

class Header:
    HEADER_SIZE = 32
    
    def __init__(self, bytes):
        self.magic = bytes[0:8]
        self.textures_count = int.from_bytes(bytes[8:8+4], 'little')
        self.offsets_offset = int.from_bytes(bytes[12:12+4], 'little')
        self.size_offset = int.from_bytes(bytes[16:16+4], 'little')
        self.flags_offset = int.from_bytes(bytes[20:20+4], 'little')
        self.idx_offset = int.from_bytes(bytes[24:24+4], 'little')
        self.info_offset = int.from_bytes(bytes[28:28+4], 'little')

class TextureEntry:
    def __init__(self, idx, offset, size, flags, info):
        self.idx = idx
        self.offset = offset
        self.size = size
        self.flags = flags
        self.info = info
        
class WtaFile:    
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        self.header = Header(byte_reader.read(Header.HEADER_SIZE))
        
        byte_reader.seek(self.header.offsets_offset)
        raw_offsets = byte_reader.read(self.header.textures_count * 4);
        offsets = [int.from_bytes(raw_offsets[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        
        byte_reader.seek(self.header.size_offset)
        raw_sizes = byte_reader.read(self.header.textures_count * 4);
        sizes = [int.from_bytes(raw_sizes[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        
        byte_reader.seek(self.header.flags_offset)
        raw_flags = byte_reader.read(self.header.textures_count * 4);
        flags = [int.from_bytes(raw_flags[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        
        byte_reader.seek(self.header.idx_offset)
        raw_idxs = byte_reader.read(self.header.textures_count * 4);
        idxs = [int.from_bytes(raw_idxs[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        
        byte_reader.seek(self.header.info_offset)
        raw_infos = byte_reader.read(self.header.textures_count * 8);
        infos = [int.from_bytes(raw_infos[i*8:i*8+8], 'little')  for i in range(0, self.header.textures_count)]
        
        self.textures = [TextureEntry(idxs[i], offsets[i], sizes[i], flags[i], infos[i]) for i in range(0, self.header.textures_count)]