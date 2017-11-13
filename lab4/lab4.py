#!/usr/bin/python
import argparse
import math

from collections import Counter
from sys import argv

from shannon_fano import shannon_fano
from ceym_compression import (write_signature, write_source_filename,
                              write_frequency_table, write_data_chunks)
from ceym_decompression import (check_signature, read_filename,
                                read_opposite_codes, read_data_chunks,
                                NotValidSignatureException)


def count_symbol_probabilities(filename):
    counter = Counter()
    file_size = 0
    with open(filename, 'rb') as f:
        for char in iter(lambda: f.read(1), b''):
            counter.update(char)
            file_size += 1
    return sorted([(char, round(quantity / file_size, 4))
                   for char, quantity in counter.items()],
                  key=lambda x: x[1], reverse=True)


def compress(source_filename, archive_filename, codes):
    write_signature(archive_filename)
    write_source_filename(archive_filename, source_filename)
    write_frequency_table(archive_filename, codes)
    write_data_chunks(archive_filename, source_filename, codes)


def decompress(archive_filename):
    try:
        position = check_signature(archive_filename)
    except NotValidSignatureException:
        print('Not .ceym archive or corrupted data!')
        return
    position, source_filename = read_filename(archive_filename, position)
    position, opposite_codes = read_opposite_codes(archive_filename, position)
    read_data_chunks(archive_filename, position,
                     source_filename, opposite_codes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--unpack', help='unpack .ceym archive')
    parser.add_argument('-s', '--show', help='show archive info')
    parser.add_argument('-n', '--name', help='specify archive name')
    parser.add_argument('-p', '--pack', help='file to packing')
    args = parser.parse_args()
    if args.unpack:
        decompress(args.unpack)
    elif args.show:
        try:
            position = check_signature(args.show)
        except NotValidSignatureException:
            print('Not .ceym archive or corrupted data!')
            exit(1)
        position, source_filename = read_filename(args.show, position)
        print('Valid .ceym archive with "{0}" file.'.format(source_filename))
    else:
        if not args.pack or not args.name:
            print('You should specify <pack> and <name> parameters!')
            exit(1)
        probs = count_symbol_probabilities(args.pack)
        codes = shannon_fano(probs)
        compress(args.pack, args.name, codes)
