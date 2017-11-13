import math

from collections import Counter

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
                     'output', opposite_codes)


if __name__ == '__main__':
    source_filename = 'input.txt'
    archive_filename = 'archive.ceym'
    probs = count_symbol_probabilities(source_filename)
    codes = shannon_fano(probs)
    compress(source_filename, archive_filename, codes)
    decompress(archive_filename)
