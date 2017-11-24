#!/usr/bin/env python
import argparse
import math
from sys import argv

from shannon_fano import shannon_fano
from ceym.frequency_counter import frequency_counter
from ceym.format import (check_signature, read_source_name,
                         write_signature, write_source_name)
from shannon_fano_packing import pack
from shannon_fano_unpacking import unpack


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--unpack', help='unpack .ceym archive')
    parser.add_argument('-s', '--show', help='show archive info')
    parser.add_argument('-n', '--name', help='specify archive name')
    parser.add_argument('-p', '--pack', help='file to packing')
    args = parser.parse_args()
    if args.unpack:
        unpack(args.unpack)
    elif args.show:
        try:
            position = check_signature(args.show)
        except NotValidSignatureException:
            print('Not .ceym archive or corrupted data!')
            exit(1)
        position, source_name = read_source_name(args.show, position)
        print('Valid .ceym archive with "{0}" file.'.format(source_name))
    else:
        if not args.pack or not args.name:
            print('You should specify <pack> and <name> parameters!')
            exit(1)
        frequencies = frequency_counter(args.pack)
        codes = shannon_fano(frequencies)
        pack(args.pack, args.name, codes)
