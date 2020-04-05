#!/usr/bin/python3

import os

class SmdEntry:    
    def __init__(self, id, number, text):
        self.id = id
        self.number = number
        self.text = text

class SmdFile:
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        count = int.from_bytes(byte_reader.read(4), 'little')
        
        self.entries = []
        for i in range(count):
            id_bytes = byte_reader.read(0x80)
            number_bytes = byte_reader.read(0x8)
            text_bytes = byte_reader.read(0x800)
            self.entries.append(SmdEntry(id_bytes.decode("utf-16-le").rstrip('\0'), int.from_bytes(number_bytes, 'little'), text_bytes.decode("utf-16-le").rstrip('\0')))
            
    def serialize(self):
        result = len(self.entries).to_bytes(4, 'little')
        for e in self.entries:
            result += e.id.encode("utf-16-le").ljust(0x80, b'\0')
            result += e.number.to_bytes(0x8, 'little')
            result += e.text.encode("utf-16-le").ljust(0x800, b'\0')
        return result