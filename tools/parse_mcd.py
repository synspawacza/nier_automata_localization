#!/usr/bin/python3

import argparse
from mcdfile import McdFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".mcd file name")

args = parser.parse_args()
file = open(args.file, "rb")

mcd = McdFile(file)

print('header: ', vars(mcd.header))

print('symbols {')
for s in mcd.symbols:
    print(vars(s))
print('} //symbols')

print('glyphs {')
for s in mcd.glyphs:
    print(vars(s))
print('} //glyphs')

print('glyph_properties {')
for s in mcd.glyph_properties:
    print(vars(s))
print('} //glyph_properties')

print('messages {')
for s in mcd.messages:
    print(vars(s))
    print('lines {')
    for l in s.lines:
        print(vars(l))
        print('texts {')
        for t in l.texts:
            print(vars(t))
            print('content {')
            for v in t.content:
                print(vars(v))
            print('} //content')
        print('} //texts')
    print('} //lines')
print('} //messages')

print('events {')
for s in mcd.events:
    print(vars(s))
print('} //events')
