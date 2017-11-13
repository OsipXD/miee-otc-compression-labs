import math

from collections import Counter

from shannon_fano import shannon_fano


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
    archive = open(archive_filename, 'wb')
    archive.write(b'.CEYM')  # signature
    archive.write(len(source_filename).to_bytes(1, 'big'))  # name_len
    archive.write(source_filename.encode())  # name
    archive.write(len(codes).to_bytes(1, 'big'))  # freq_table_len
    for symbol, code in codes.items():  # freq_table_chunks
        archive.write(symbol.to_bytes(1, 'big'))  # symbol
        archive.write(len(code).to_bytes(1, 'big'))  # n_significant_bits
        code_len = math.ceil(len(code) / 8)  # significant_bits
        archive.write(int(code, 2).to_bytes(code_len, 'big'))
    with open(source_filename, 'rb') as source:
        buff = ''
        end_of_file = False
        while not end_of_file:  # data_chunks
            while len(buff) <= 255 and not end_of_file:
                char = source.read(1)
                if char == b'':
                    end_of_file = True
                    break
                buff += codes[ord(char)]
            if len(buff) > 255:
                to_archive, buff = buff[:255], buff[255:]
            else:
                to_archive = buff
            archive.write(len(to_archive).to_bytes(1, 'big'))
            chunk_bytes_len = math.ceil(len(to_archive) / 8)
            archive.write(int(to_archive, 2).to_bytes(chunk_bytes_len, 'big'))
    archive.close()


def decompress(archive_filename):
    archive = open(archive_filename, 'rb')
    signature = archive.read(5)
    if signature != b'.CEYM':
        print('Not .ceym archive or corrupted data!')
        return
    name_len = int.from_bytes(archive.read(1), 'big')
    source_filename = archive.read(name_len).decode()
    freq_table_len = int.from_bytes(archive.read(1), 'big')
    opposite_codes = {}
    for table_chunk in range(freq_table_len):
        symbol = int.from_bytes(archive.read(1), 'big')
        n_significant_bits = int.from_bytes(archive.read(1), 'big')
        bytes_to_read = math.ceil(n_significant_bits / 8)
        bytes_ = int.from_bytes(archive.read(bytes_to_read), 'big')
        binary = '0' * 7 + bin(bytes_)[2:]
        significant_bits = binary[-(n_significant_bits):]
        opposite_codes[significant_bits] = symbol
    with open(source_filename, 'wb') as source:
        end_of_file = False
        buff = ''
        while not end_of_file:
            char = archive.read(1)
            if char == b'':
                end_of_file = True
                break
            chunk_bit_len = int.from_bytes(char, 'big')
            chunk_byte_len = math.ceil(chunk_bit_len / 8)
            raw_data = archive.read(chunk_byte_len)
            binary = '0' * 7 + bin(int.from_bytes(raw_data, 'big'))[2:]
            from_archive = binary[-(chunk_bit_len):]
            while len(from_archive):
                buff += from_archive[0]
                from_archive = from_archive[1:]
                if buff in opposite_codes:
                    source.write(opposite_codes[buff].to_bytes(1, 'big'))
                    buff = ''
    archive.close()


if __name__ == '__main__':
    source_filename = 'input.txt'
    archive_filename = 'archive.ceym'
    probs = count_symbol_probabilities(source_filename)
    codes = shannon_fano(probs)
    compress(source_filename, archive_filename, codes)
    decompress(archive_filename)
