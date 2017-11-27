import struct

from ceym.format import (check_signature, read_source_name,
                         write_signature, write_source_name,
                         NotValidSignatureError)


def pack(source_name, archive_name=None):
    if archive_name is None:
        archive_name = source_name.rpartition('.')[0] + '.ceym'
    write_signature(archive_name)
    write_source_name(archive_name, source_name)
    # packing


def pack_bytes(bytes):
	counter = 0
	sequence = []
	packed = []

	for byte in bytes:
		if counter == 0:
			last_byte = byte
			counter = 1
			continue

		if byte == last_byte:
			if sequence:
				packed += sign_sequence(sequence)
				sequence = []
			counter += 1
		else:
			if counter == 1:
				sequence += [last_byte]
			else:
				packed += sign_byte(counter, last_byte)
				counter = 1

		# print(chr(byte) + ' > ' + str(packed))
		# print('sequence: ' + str(sequence) + "; counter: " + str(counter))
		last_byte = byte

	packed += sign_sequence(sequence + [byte]) if sequence else sign_byte(counter, last_byte)

	return packed


def sign_sequence(sequence):
	prefix = [0x00, len(sequence)]
	part = prefix + sequence

	return part


def sign_byte(count, byte):
	return [count, byte]


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
