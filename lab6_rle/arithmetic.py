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
	count = 0
	sequence = []
	packed = []

	for byte in bytes:
		if count == 0:
			last_byte = byte
			count = 1
			continue

		if byte == last_byte:
			if sequence:
				packed += sign_sequence(sequence)
				sequence = []
			count += 1
		else:
			if count == 1:
				sequence += [last_byte]
			else:
				packed += sign_byte(count, last_byte)
				count = 1

		# print(chr(byte) + ' > ' + str(packed))
		# print('sequence: ' + str(sequence) + "; count: " + str(count))
		last_byte = byte

	packed += sign_sequence(sequence + [byte]) if sequence else sign_byte(count, last_byte)

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


def unpack_bytes(bytes):
	count = 0
	sequence = []
	read_sequence = False
	unpacked = []

	for byte in bytes:
		if count == 0:
			if byte == 0x00:
				read_sequence = True
				continue

			count = byte
			continue

		if read_sequence:
			sequence.append(byte)
			if len(sequence) == count:
				read_sequence = False
				count = 0
				unpacked += sequence
		else:
			unpacked += [byte] * count
			count = 0 

	return unpacked