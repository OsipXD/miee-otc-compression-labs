from ceym.format import (check_signature, read_source_name,
                         write_signature, write_source_name,
                         NotValidSignatureError)


def pack(source_name, archive_name=None):
    if archive_name is None:
        archive_name = source_name.rpartition(' ')[0] + '.ceym'
    write_signature(archive_name)
    write_source_name(archive_name, source_name)
    # packing


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
