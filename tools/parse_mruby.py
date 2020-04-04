#!/usr/bin/python3

import argparse
from mrubybytecode import MrubyFile
from mrubybytecode import IrepSection

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".bin file name")

args = parser.parse_args()
file = open(args.file, "rb")

mruby = MrubyFile(file)

def opcode(value):
    return value & 0x7F
def get_bx(value):
    return (value >> 7) & 0xFFFF
def get_a(value):
    return (value >> 23)
    
OP_SETCONST = 0x12
OP_ARRAY = 0x37
OP_STRING = 0x3d

for section in mruby.sections:
    if isinstance(section, IrepSection):
        for sidx, segment in enumerate(section.segments):
            for iidx, instr in enumerate(segment.instructions):
                array_size = 0
                if(instr == 0x804437): #0x804437 OP_ARRAY 1 1 8
                    array_size = 8
                elif(instr == 0x804337): #0x804337 OP_ARRAY 1 1 6
                    array_size = 6
                else:
                    continue
                    
                symbol_instr = segment.instructions[iidx+1]
                assert(opcode(symbol_instr) == OP_SETCONST)
                symbol = segment.symbols[get_bx(symbol_instr)]
                
                messages = ['']*array_size
                for str_instr in segment.instructions[iidx-array_size:iidx]:
                    assert(opcode(str_instr) == OP_STRING)
                    messages[get_a(str_instr)-1] = segment.pool[get_bx(str_instr)].value
                print(symbol+'\t'+'\t'.join([repr(m) for m in messages[:6]]))
                    

#TODO: extract strings = find string arrays of size >= 6
