import math


def write_signature(archive_filename):
    with open(archive_filename, 'wb') as archive:
        archive.write(b'.CEYM')


def write_source_filename(archive_filename, source_filename):
    with open(archive_filename, 'ab') as archive:
        archive.write(len(source_filename).to_bytes(1, 'big'))
        archive.write(source_filename.encode())


def write_frequency_table(archive_filename, codes):
    with open(archive_filename, 'ab') as archive:
        archive.write(len(codes).to_bytes(1, 'big'))
        for byte, code in codes.items():
            archive.write(byte.to_bytes(1, 'big'))
            archive.write(len(code).to_bytes(1, 'big'))
            code_len = math.ceil(len(code) / 8)
            archive.write(int(code, 2).to_bytes(code_len, 'big'))


def write_data_chunks(archive_filename, source_filename, codes):
    archive = open(archive_filename, 'ab')
    with open(source_filename, 'rb') as source:
        buff = ''
        for byte in iter(lambda: source.read(1), b''):
            buff += codes[ord(byte)]
            if len(buff) > 255:
                to_archive, buff = buff[:255], buff[255:]
                write_chunk(archive, to_archive)
        if buff != b'':
            write_chunk(archive, buff)
    archive.close()


def write_chunk(file_descriptor, buff):
    file_descriptor.write(len(buff).to_bytes(1, 'big'))
    chunk_byte_len = math.ceil(len(buff) / 8)
    file_descriptor.write(int(buff, 2).to_bytes(chunk_byte_len, 'big'))
