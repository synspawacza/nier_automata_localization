#!/usr/bin/python3

#based on https://gist.github.com/Wunkolo/213aa61eb0c874172aec97ebb8ab89c2
#based on https://github.com/xxk-i/DATrepacker/blob/master/dat_utils.py

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
        self.crc_table_offset = int.from_bytes(bytes[24:24+4], 'little')
        self.unknown = bytes[28:]

class FileEntry:
    """File entry in DAT file, split over multiple tables in actual file"""
    
    def __init__(self, name, ext, offset, size, byte_reader):
        self.name = name
        self.extension = ext
        self.offset = offset
        self.size = size
        byte_reader.seek(offset)
        self.bytes = byte_reader.read(size)

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
        
        byte_reader.seek(self.header.crc_table_offset)
        self.crc_table = byte_reader.read(file_offsets[0] - self.header.crc_table_offset)
        
        self.files = [FileEntry(names[i], exts[i], file_offsets[i], file_sizes[i], byte_reader) for i in range(0, self.header.file_count)]
    
    
    def serialize(self):
        result = bytearray(self.header.magic + b'\0' * (Header.HEADER_SIZE-4)) # placeholder
        file_count = len(self.files)
        result[4:4+4] = file_count.to_bytes(4, 'little')
        
        file_table_offset = len(result)
        result[8:8+4] = file_table_offset.to_bytes(4, 'little')
        result += b'\0' * 4 * file_count # placeholder
        
        ext_table_offset = len(result)
        result[12:12+4] = ext_table_offset.to_bytes(4, 'little')
        for file in self.files:
            result += file.name.split('.')[-1].encode("utf-8").ljust(4, b'\0')
        
        name_table_offset = len(result)
        result[16:16+4] = name_table_offset.to_bytes(4, 'little')
        filename_len = max([len(f.name) for f in self.files])+1
        result += filename_len.to_bytes(4, 'little')
        for file in self.files:
            result += file.name.encode("utf-8").ljust(filename_len, b'\0')
        
        #pad with zeroes to mod 4
        padding_length = 4-(len(result) % 4)
        if padding_length < 4:
            result += b'\0' * padding_length
            
        size_table_offset = len(result)
        result[20:20+4] = size_table_offset.to_bytes(4, 'little')
        for file in self.files:
            result += len(file.bytes).to_bytes(4, 'little')
        
        crc_table_offset = len(result)
        result[24:24+4] = crc_table_offset.to_bytes(4, 'little')
        result += self.crc_table # keep the same CRC
        
        #pad with zeroes to mod 16
        padding_length = 16-(len(result) % 16)
        if padding_length < 16:
            result += b'\0' * padding_length
        
        file_offset_offset = file_table_offset;
        for file in self.files:
            file_offset = len(result)
            result[file_offset_offset:file_offset_offset+4]=file_offset.to_bytes(4, 'little')
            file_offset_offset += 4
            result += file.bytes
            #pad with zeroes to mod 16
            padding_length = 16-(len(result) % 16)
            if padding_length < 16:
                result += b'\0' * padding_length

        return result