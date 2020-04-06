#!/usr/bin/python3

import os

class TmdEntry:    
    def __init__(self, id, text):
        self.id = id
        self.text = text

class TmdFile:
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        count = int.from_bytes(byte_reader.read(4), 'little')
        
        self.entries = []
        for i in range(count):
            idsize = int.from_bytes(byte_reader.read(4), 'little')
            id_bytes = byte_reader.read(idsize*2)
            id = id_bytes.decode("utf-16-le").rstrip('\0')
            textsize = int.from_bytes(byte_reader.read(4), 'little')
            text_bytes = byte_reader.read(textsize*2)
            text = text_bytes.decode("utf-16-le").rstrip('\0')
            self.entries.append(TmdEntry(id, text))
            
    def serialize(self):
        result = len(self.entries).to_bytes(4, 'little')
        for e in self.entries:
            result += len(e.id+'\0').to_bytes(4, 'little')
            result += (e.id+'\0').encode("utf-16-le")
            result += len(e.text+'\0').to_bytes(4, 'little')
            result += (e.text+'\0').encode("utf-16-le")
        return result