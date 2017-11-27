import struct

from ceym.format import (check_signature, read_source_name,
                         write_signature, write_source_name,
                         NotValidSignatureError)
from ceym.frequency_counter import frequency_counter


def pack(source_name, archive_name=None):
    if archive_name is None:
        archive_name = source_name.rpartition(' ')[0] + '.ceym'
    write_signature(archive_name)
    write_source_name(archive_name, source_name)
    frequencies = frequency_counter(source_name)
    write_frequency_table(archive_name, frequencies)


def write_frequency_table(archive_name, frequencies):
    with open(archive_name, 'ab') as archive:
        archive.write(len(frequencies).to_bytes(2, 'big'))
        for code, frequency in frequencies:
            archive.write(code.to_bytes(1, 'big'))
            archive.write(struct.pack('>d', frequency))


def unpack(archive_name, override_name=None):
    try:
        position = check_signature(archive_name)
    except NotValidSignatureError:
        print('Not valid ceym archive!')
        return
    position, source_name = read_source_name(archive_name, position)
    if override_name is not None:
        source_name = override_name
    # unpacking
