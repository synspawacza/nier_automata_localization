#!/usr/bin/python3

#based on https://gist.github.com/Wunkolo/213aa61eb0c874172aec97ebb8ab89c2

import os

class Header:
    """Dat file header"""
    HEADER_SIZE = 32
    
    def __init__(self, bytes):
        self.magic = bytes[0:4]
        self.file_count = int.from_bytes(bytes[4:4+4], 'little')
        self.file_table_offset = int.from_bytes(bytes[8:8+4], 'little')
        self.ext_table_offset = int.from_bytes(bytes[12:12+4], 'little')
        self.name_table_offset = int.from_bytes(bytes[16:16+4], 'little')
        self.size_table_offset = int.from_bytes(bytes[20:20+4], 'little')
        self.unknown = bytes[24:]

class FileEntry:
    """File entry in DAT file, split over multiple tables in actual file"""
    
    def __init__(self, name, ext, offset, size):
        self.name = name
        self.extension = ext
        self.offset = offset
        self.size = size

class DatArchive:
    """Dat archive"""
    
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        self.header = Header(byte_reader.read(Header.HEADER_SIZE))
        
        byte_reader.seek(self.header.file_table_offset)
        raw_offsets = byte_reader.read(self.header.file_count * 4);
        file_offsets = [int.from_bytes(raw_offsets[i*4:i*4+4], 'little')  for i in range(0, self.header.file_count)]
        
        byte_reader.seek(self.header.ext_table_offset)
        raw_exts = byte_reader.read(self.header.file_count * 4);
        exts = [raw_exts[i*4:i*4+4].decode("utf-8").rstrip('\0')  for i in range(0, self.header.file_count)]
        
        byte_reader.seek(self.header.size_table_offset)
        raw_sizes = byte_reader.read(self.header.file_count * 4);
        file_sizes = [int.from_bytes(raw_sizes[i*4:i*4+4], 'little')  for i in range(0, self.header.file_count)]
        
        
        byte_reader.seek(self.header.name_table_offset)
        self.max_filename_len = int.from_bytes(byte_reader.read(4), 'little')
        raw_names = byte_reader.read(self.header.file_count * self.max_filename_len);
        names = [raw_names[i*self.max_filename_len:(i+1)*self.max_filename_len].decode("utf-8").rstrip('\0')  for i in range(0, self.header.file_count)]
        
        self.files = [FileEntry(names[i], exts[i], file_offsets[i], file_sizes[i]) for i in range(0, self.header.file_count)]
    
    def hex_representation(self):
        #return self.max_filename_len
        return [vars(f) for f in self.files]
        #return vars(self.header)