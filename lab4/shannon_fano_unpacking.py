import math

from ceym.format import (check_signature, read_source_name,
                         NotValidSignatureError)


def unpack(archive_filename):
    try:
        position = check_signature(archive_filename)
    except NotValidSignatureError:
        print('Not .ceym archive or corrupted data!')
        return
    position, source_filename = read_source_name(archive_filename, position)
    position, opposite_codes = read_opposite_codes(archive_filename, position)
    read_data_chunks(archive_filename, position,
                     source_filename, opposite_codes)


def read_opposite_codes(archive_filename, position):
    opposite_codes = {}
    with open(archive_filename, 'rb') as archive:
        archive.seek(position)
        freq_table_len = int.from_bytes(archive.read(1), 'big')
        for table_chunk in range(freq_table_len):
            symbol = int.from_bytes(archive.read(1), 'big')
            n_significant_bits = int.from_bytes(archive.read(1), 'big')
            bytes_to_read = math.ceil(n_significant_bits / 8)
            bytes_ = int.from_bytes(archive.read(bytes_to_read), 'big')
            binary = '0' * 7 + bin(bytes_)[2:]
            significant_bits = binary[-(n_significant_bits):]
            opposite_codes[significant_bits] = symbol
        position = archive.tell()
    return position, opposite_codes


def read_data_chunks(archive_filename, position,
                     source_filename, opposite_codes):
    with open(source_filename, 'wb') as source:
        buff = ''
        for chunk in iter_data_chunks(archive_filename, position):
            while len(chunk):
                buff += chunk[0]
                chunk = chunk[1:]
                if buff in opposite_codes:
                    source.write(opposite_codes[buff].to_bytes(1, 'big'))
                    buff = ''


def iter_data_chunks(archive_filename, position):
    with open(archive_filename, 'rb') as archive:
        archive.seek(position)
        byte = archive.read(1)
        while byte != b'':
            chunk_bit_len = int.from_bytes(byte, 'big')
            chunk_byte_len = math.ceil(chunk_bit_len / 8)
            data = archive.read(chunk_byte_len)
            binary = '0' * 7 + bin(int.from_bytes(data, 'big'))[2:]
            yield binary[-(chunk_bit_len):]
            byte = archive.read(1)
