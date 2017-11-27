def pack(source_name, archive_name=None):
    if archive_name is None:
        archive_name = source_name.rpartition(' ')[0] + '.ceym'
    # packing


def unpack(archive_name, override_name=None):
    # get source_name from archive
    if override_name is not None:
        source_name = override_name
    # unpacking
