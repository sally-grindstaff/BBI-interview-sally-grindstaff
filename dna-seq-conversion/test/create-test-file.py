#!/usr/bin/env python

b = '00000000111000001100000101111111'
my_bytearray = bytearray(int(b[x:x+8], 2) for x in range(0, len(b), 8))

with open('binary_test_input.bin', 'wb') as fh:
    fh.write(my_bytearray)
