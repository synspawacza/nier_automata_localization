#!/usr/bin/python3

import struct

#based on https://zenhax.com/viewtopic.php?t=1502&p=8181
#based on https://github.com/Kerilk/bayonetta_tools/blob/master/binary_templates/Bayonetta%202%20mcd%20base.bt

class Header:
    HEADER_SIZE = 40
    
    def __init__(self, bytes):
        self.messages_offset = int.from_bytes(bytes[0:0+4], 'little')
        self.messages_count = int.from_bytes(bytes[4:4+4], 'little')
        self.symbols_offset = int.from_bytes(bytes[8:8+4], 'little')
        self.symbols_count = int.from_bytes(bytes[12:12+4], 'little')
        self.glyphs_offset = int.from_bytes(bytes[16:16+4], 'little')
        self.glyphs_count = int.from_bytes(bytes[20:20+4], 'little')
        self.glyphprops_offset = int.from_bytes(bytes[24:24+4], 'little')
        self.glyphprops_count = int.from_bytes(bytes[28:28+4], 'little')
        self.events_offset = int.from_bytes(bytes[32:32+4], 'little')
        self.events_count = int.from_bytes(bytes[36:36+4], 'little')
        
class GlyphProperties:
    ENTRY_SIZE = 20
    def __init__(self, bytes):
        self.id = int.from_bytes(bytes[0:0+4], 'little')
        self.width = struct.unpack('f', bytes[4:4+4])[0]
        self.height = struct.unpack('f', bytes[8:8+4])[0]
        self.kern_below = struct.unpack('f', bytes[12:12+4])[0]
        self.kern_horiz = struct.unpack('f', bytes[16:16+4])[0]
        
class Symbol:
    ENTRY_SIZE = 8
    def __init__(self, bytes):
        self.font = int.from_bytes(bytes[0:0+2], 'little')
        self.char = bytes[2:2+2].decode("utf-16-le")
        self.glyph = int.from_bytes(bytes[4:4+4], 'little')
        
class Glyph:
    ENTRY_SIZE = 40
    def __init__(self, bytes):
        self.texture = int.from_bytes(bytes[0:0+4], 'little')
        self.u1 = struct.unpack('f', bytes[4:4+4])[0]
        self.v1 = struct.unpack('f', bytes[8:8+4])[0]
        self.u2 = struct.unpack('f', bytes[12:12+4])[0]
        self.v2 = struct.unpack('f', bytes[16:16+4])[0]
        self.width = struct.unpack('f', bytes[20:20+4])[0]
        self.height = struct.unpack('f', bytes[24:24+4])[0]
        self.spacing_above = struct.unpack('f', bytes[28:28+4])[0]
        self.spacing_below = struct.unpack('f', bytes[32:32+4])[0]
        self.spacing_horiz = struct.unpack('f', bytes[36:36+4])[0]
        
        
class Message:
    ENTRY_SIZE = 16
    def __init__(self, bytes):
        self.lines_offset = int.from_bytes(bytes[0:0+4], 'little')
        self.lines_count = int.from_bytes(bytes[4:4+4], 'little')
        self.seq_number = int.from_bytes(bytes[8:8+4], 'little')
        self.event_id = int.from_bytes(bytes[12:12+4], 'little')
        self.lines = [] #to be filled later
        
class Line:
    ENTRY_SIZE = 20
    def __init__(self, bytes):
        self.texts_offset = int.from_bytes(bytes[0:0+4], 'little')
        self.texts_count = int.from_bytes(bytes[4:4+4], 'little')
        self.spacing_below = struct.unpack('f', bytes[8:8+4])[0]
        self.spacing_horiz = struct.unpack('f', bytes[12:12+4])[0]
        self.meta = bytes[16:16+4]
        self.texts = []
        
class Text:
    ENTRY_SIZE = 24
    def __init__(self, bytes):
        self.content_offset = int.from_bytes(bytes[0:0+4], 'little')
        self.padding = int.from_bytes(bytes[4:4+4], 'little')
        self.length1 = int.from_bytes(bytes[8:8+4], 'little')
        self.length2 = int.from_bytes(bytes[12:12+4], 'little')
        self.spacing_below = struct.unpack('f', bytes[16:16+4])[0]
        self.spacing_horiz = struct.unpack('f', bytes[20:20+4])[0]
        self.content =  []
        
class StringChars:
    ENTRY_SIZE = 4
    def __init__(self, bytes):
        self.char_id = int.from_bytes(bytes[0:0+2], 'little')
        self.padding = int.from_bytes(bytes[2:2+2], 'little', signed=True)
        
class Event:
    ENTRY_SIZE = 40
    def __init__(self, bytes):
        self.id = int.from_bytes(bytes[0:0+4], 'little')
        self.idx = int.from_bytes(bytes[4:4+4], 'little', signed=True)
        self.name = bytes[8:8+32].decode("utf-8").rstrip('\0')
        
        
class McdFile:
    def __init__(self, byte_reader):
        self.byte_reader = byte_reader
        
        byte_reader.seek(0)
        self.header = Header(byte_reader.read(Header.HEADER_SIZE))
        
        byte_reader.seek(self.header.symbols_offset)
        self.symbols = []
        for i in range(self.header.symbols_count):
            raw_symbol = byte_reader.read(Symbol.ENTRY_SIZE)
            self.symbols.append(Symbol(raw_symbol))
        
        byte_reader.seek(self.header.glyphs_offset)
        self.glyphs = []
        for i in range(self.header.glyphs_count):
            raw_glyph = byte_reader.read(Glyph.ENTRY_SIZE)
            self.glyphs.append(Glyph(raw_glyph))
        
        byte_reader.seek(self.header.glyphprops_offset)
        self.glyph_properties = []
        for i in range(self.header.glyphprops_count):
            raw_font = byte_reader.read(GlyphProperties.ENTRY_SIZE)
            self.glyph_properties.append(GlyphProperties(raw_font))
            
        byte_reader.seek(self.header.messages_offset)
        self.messages = []
        for i in range(self.header.messages_count):
            raw_font = byte_reader.read(Message.ENTRY_SIZE)
            self.messages.append(Message(raw_font))
            
        for msg in self.messages:
            byte_reader.seek(msg.lines_offset)
            for i in range(msg.lines_count):
                msg.lines.append(Line(byte_reader.read(Line.ENTRY_SIZE)))
                
        for msg in self.messages:
            for line in msg.lines:
                byte_reader.seek(line.texts_offset)
                for i in range(line.texts_count):
                    line.texts.append(Text(byte_reader.read(Text.ENTRY_SIZE)))
                
        for msg in self.messages:
            for line in msg.lines:
                for text in line.texts:
                    byte_reader.seek(text.content_offset)
                    for i in range(int((text.length1-1)/2)):
                        text.content.append(StringChars(byte_reader.read(StringChars.ENTRY_SIZE)))
        
        byte_reader.seek(self.header.events_offset)
        self.events = []
        for i in range(self.header.events_count):
            self.events.append(Event(byte_reader.read(Event.ENTRY_SIZE)))
            
        #byte_reader.seek(self.header.size_offset)
        #raw_sizes = byte_reader.read(self.header.textures_count * 4);
        #sizes = [int.from_bytes(raw_sizes[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        #
        #byte_reader.seek(self.header.flags_offset)
        #raw_flags = byte_reader.read(self.header.textures_count * 4);
        #flags = [int.from_bytes(raw_flags[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        #
        #byte_reader.seek(self.header.idx_offset)
        #raw_idxs = byte_reader.read(self.header.textures_count * 4);
        #idxs = [int.from_bytes(raw_idxs[i*4:i*4+4], 'little')  for i in range(0, self.header.textures_count)]
        #
        #byte_reader.seek(self.header.info_offset)
        #raw_infos = byte_reader.read(self.header.textures_count * 8);
        #infos = [int.from_bytes(raw_infos[i*8:i*8+8], 'little')  for i in range(0, self.header.textures_count)]
        #
        #self.textures = [TextureEntry(idxs[i], offsets[i], sizes[i], flags[i], infos[i]) for i in range(0, self.header.textures_count)]
