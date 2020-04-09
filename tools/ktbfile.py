#!/usr/bin/python3

import os

class KtbEntry:    
    def __init__(self, left, right, kerning):
        self.left = left
        self.right = right
        self.kerning = kerning

class KtbFile:
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        count = int.from_bytes(byte_reader.read(2), 'little')
        
        self.entries = []
        for i in range(count):
            left = byte_reader.read(2)
            right = byte_reader.read(2)
            kerning = byte_reader.read(2)
            self.entries.append(KtbEntry(left.decode("utf-16-le"), right.decode("utf-16-le"), int.from_bytes(kerning, 'little', signed=True)))
            
    def serialize(self):
        result = len(self.entries).to_bytes(2, 'little')
        for e in self.entries:
            result += e.left.encode("utf-16-le").ljust(2, b'\0')
            result += e.right.encode("utf-16-le").ljust(2, b'\0')
            result += e.kerning.to_bytes(2, 'little', signed=True)
        return result