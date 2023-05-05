#!/usr/bin/env python

import argparse
from pathlib import Path
from typing import TextIO

def get_args():
    parser = argparse.ArgumentParser(description='Converts encoded DNA sequencing file to FASTQ format. Output file will be written to current working directory using the input file name as a prefix, unless an output path is supplied.')
    parser.add_argument('-i', '--input_file', help='Path to input file. Should be a binary file that uses the encoding described in readme.md (one byte per base, first two bits encode for base identity and last six bits encode an integer that represents the quality score).', required=True, type=str)
    parser.add_argument('-L', '--length', help='Length of reads (pieces). Each read will have L bases.', required=True, type=int)
    parser.add_argument('-o', '--output_file', help='Path to output file. Recommend that filename use .fastq or .fq as extension.', required=False, type=str)
    return parser.parse_args()

def parse_byte(byte_str: str):
    '''Takes in a string representing one 8-bit byte, and returns the corresponding DNA base and ASCII quality score'''
    base_bin = byte_str[0:2] # the first two bits encode for the base
    base_letter = base_decode_dict[base_bin]
    qual_bin = byte_str[2:] # the last six bits encode for the qual score
    qual_score = decode_qual(qual_bin)
    return base_letter, qual_score

def decode_qual(qual_bin: str) -> str:
    '''Takes a string representing an integer in 6-bit binary notation, and returns corresponding Phred+33 quality score in ASCII format'''
    # convert from binary to int
    qual_int = int(qual_bin, 2)
    # add 33
    qual_int += 33
    # convert from int to ascii
    qual_score = chr(qual_int)
    return qual_score

def write_piece(piece_index: int, bases: str, quals: str, out_fh: TextIO):
    '''Writes entry for a piece of DNA to FASTQ file'''
    out_fh.write(f'@READ_{str(piece_index)}\n') # header line
    out_fh.write(f'{bases}\n') # sequence line
    out_fh.write(f'+READ_{str(piece_index)}\n') # plus line
    out_fh.write(f'{quals}\n') # quality line

# create dictionary for base decoding. Keys are two-bit codes and values are corresponding bases
base_decode_dict = {
    '00': 'A',
    '01': 'C',
    '10': 'G',
    '11': 'T'
}

args = get_args()

# convert input file arg to path object
input_path = Path(args.input_file)

# if no output path supplied, create output path
if args.output_file is None:
    output_path = Path.cwd() / f'{input_path.stem}.fastq'
else: # otherwise, convert output file arg to path object
    output_path = Path(args.output_file)


with open(input_path, 'rb') as in_fh, open(output_path, 'w') as out_fh:
    piece = in_fh.read(args.length) # read L bytes at a time (L bytes represent one piece of DNA)
    i = 1 # piece index
    while piece: # loop through input file; will break when piece becomes Falsey due to EOF
        piece_bases = [] # initialize list to build base sequence
        piece_quals = [] # initialize list to build quality score sequence
        for byte in piece:
            byte_str = (bin(byte)[2:].rjust(8, '0')) # convert the byte from int into a string of 8 1s and 0s. This will allow me to easily parse the byte.
            base, qual = parse_byte(byte_str) # get DNA base and quality score in ASCII format
            piece_bases.append(base) # add DNA base and quality score to their respective lists
            piece_quals.append(qual)
        piece_bases_str = ''.join(piece_bases) # join the list of bases into a string for this piece of DNA
        piece_quals_str = ''.join(piece_quals) # join the list of quality scores into a string for this piece of DNA
        write_piece(i, piece_bases_str, piece_quals_str, out_fh) # write entry out to fastq file
        piece = in_fh.read(args.length) # iterate
        i += 1 # increment the piece index

