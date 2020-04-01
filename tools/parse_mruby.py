#!/usr/bin/python3

import argparse
from mrubybytecode import MrubyFile
from mrubybytecode import UnknownSection

parser = argparse.ArgumentParser()
parser.add_argument("file", help=".bin file name")

args = parser.parse_args()
file = open(args.file, "rb")

mruby = MrubyFile(file)

def instruction(value):    
    opcode_strings = [
    'OP_NOP',
    'OP_MOVE {1} {4}',
    'OP_LOADL {1} {2}',
    'OP_LOADI {1} {3}',
    'OP_LOADSYM {1} {2}',
    'OP_LOADNIL {1}',
    'OP_LOADSELF {1}',
    'OP_LOADT {1}',
    'OP_LOADF {1}',
    'OP_GETGLOBAL {1} {2}',
    'OP_SETGLOBAL {1} {2}',
    'OP_GETSPECIAL {1} {2}',
    'OP_SETSPECIAL {1} {2}',
    'OP_GETIV {1} {2}',
    'OP_SETIV {1} {2}',
    'OP_GETCV {1} {2}',
    'OP_SETCV {1} {2}',
    'OP_GETCONST {1} {2}',
    'OP_SETCONST {1} {2}',
    'OP_GETMCNST {1} {2}',
    'OP_SETMCNST {1} {2}',
    'OP_GETUPVAR {1} {4} {5}',
    'OP_SETUPVAR {1} {4} {5}',
    'OP_JMP {3}',
    'OP_JMPIF {1} {3}',
    'OP_JMPNOT {1} {3}',
    'OP_ONERR {3}',
    'OP_RESCUE {1}',
    'OP_POPERR {1}',
    'OP_RAISE {1}',
    'OP_EPUSH {2}',
    'OP_EPOP {1}',
    'OP_SEND {1} {4} {5}',
    'OP_SENDB {1} {4} {5}',
    'OP_FSEND {1} {4} {5}',
    'OP_CALL {1} {4} {5}',
    'OP_SUPER {1} {4} {5}',
    'OP_ARGARY {1} {2}',
    'OP_ENTER {0}',
    'OP_KARG {1} {4} {5}',
    'OP_KDICT {1} {5}',
    'OP_RETURN {1} {4}',
    'OP_TAILCALL {1} {4} {5}',
    'OP_BLKPUSH {1} {2}',
    'OP_ADD {1} {4} {5}',
    'OP_ADDI {1} {4} {5}',
    'OP_SUB {1} {4} {5}',
    'OP_SUBI {1} {4} {5}',
    'OP_MUL {1} {4} {5}',
    'OP_DIV {1} {4} {5}',
    'OP_EQ {1} {4} {5}',
    'OP_LT {1} {4} {5}',
    'OP_LE {1} {4} {5}',
    'OP_GT {1} {4} {5}',
    'OP_GE {1} {4} {5}',
    'OP_ARRAY {1} {4} {5}',
    'OP_ARYCAT {1} {4}',
    'OP_ARYPUSH {1} {4}',
    'OP_AREF {1} {4} {5}',
    'OP_ASET {1} {4} {5}',
    'OP_APOST {1} {4} {5}',
    'OP_STRING {1} {2}',
    'OP_STRCAT {1} {4}',
    'OP_HASH {1} {4} {5}',
    'OP_LAMBDA {0}',
    'OP_RANGE {1} {4} {5}',
    'OP_OCLASS {1}',
    'OP_CLASS {1} {4}',
    'OP_MODULE {1} {4}',
    'OP_EXEC {1} {2}',
    'OP_METHOD {1} {4}',
    'OP_SCLASS {1} {4}',
    'OP_TCLASS {1}',
    'OP_DEBUG {1}',
    'OP_STOP',
    'OP_ERR {2}',
    'OP_RSVD1',
    'OP_RSVD2',
    'OP_RSVD3',
    'OP_RSVD4',
    'OP_RSVD5']
    
    opcode = value & 0x7F
    ax = value >> 7
    a = ax >> 16
    bx = ax & 0xFFFF
    sbx = bx
    if sbx >= 0x8000: sbx = -(sbx - 0x8000)
    b = bx >> 7
    c = bx & 0x7F
    format_str = opcode_strings[opcode]
    return hex(value) + ' ' + format_str.format(ax, a, bx, sbx, b, c)
    
    

print("header: ", vars(mruby.header))
print("sections:")
for section in mruby.sections:
    if isinstance(section, UnknownSection):
        print("unknown section: ", section.bytes)
    else:
        print("irep section: ", section.magic, ' size: ', section.size, 'version: ', section.version)
        for segment in section.segments:
            print("segment {");
            print('size:', segment.size, 'nlocals:', segment.nlocals, 'nregs:', segment.nregs, 'rlen:', segment.rlen, 'symbols:', segment.symbols);
            print('instructions {');
            for instr in segment.instructions:
                print(instruction(instr))
            print('} //instructions');
            print('pool {');
            for pool_val in segment.pool:
                print(vars(pool_val));
            print('} //pool');
            print("} //segment");

#TODO: extract strings = find string arrays of size >= 6
