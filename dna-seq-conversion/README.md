# DNA sequence conversion

This Python program converts a binary file encoding sequencing information to a FASTQ file.

## Binary file structure
- each read is represented by L consecutive bytes, and reads appear consecutively
- the first 2 bits of each byte represent the base:  
  00 - A  
  01 - C  
  10 - G  
  11 - T
- the last 6 bits of each byte represent an integer, which is the quality score for that byte's base

## FASTQ
The resulting FASTQ uses Phred+33 encoding

## Requirements
- Python 3

## How to use
Run dna-seq-conversion.py from the command line:
./dna-seq-conversion.py [-h] -i INPUT_FILE -L LENGTH [-o OUTPUT_FILE]
Run ./dna-seq-conversion.py -h for more details.
