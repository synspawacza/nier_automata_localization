#!/usr/bin/python3

import argparse
import itertools
from mcdfile import McdFile

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".mcd file name")

args = parser.parse_args()
file = open(args.file, "rb")

mcd = McdFile(file)

#using '{' and '}' for tagging -hopefully it doesn't break anything

for s in mcd.messages:
    matching_events = list(filter(lambda e: e.id == s.event_id, mcd.events))
    assert(len(matching_events) == 1)
    event = matching_events[0].name
    
    result = ''
    for l in s.lines:
        for t in l.texts:
            for v in t.content:
                if v.char_id < 0x8000:
                    result += mcd.symbols[v.char_id].char
                elif v.char_id == 0x8001:
                    result += ' '
                else:
                    result += '{unknown'+str(v.char_id)+'}'
            if len(l.texts) > 1: result += '{nexttext}'
        if len(s.lines) > 1: result += '{nextline}'
    print(event+'\t'+repr(result)+'\t'+args.file)
