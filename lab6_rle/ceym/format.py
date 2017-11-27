SIGNATURE = b'.CEYM'


def write_signature(archive_name):
    with open(archive_name, 'wb') as archive:
        archive.write(SIGNATURE)


def write_source_name(archive_name, source_name):
    if len(source_name) > 255:
        raise TooLongFilenameError('should be shorter than 256 characters')
    with open(archive_name, 'ab') as archive:
        archive.write(len(source_name).to_bytes(1, 'big'))
        archive.write(source_name.encode())


def check_signature(archive_name):
    with open(archive_name, 'rb') as archive:
        if archive.read(len(SIGNATURE)) != SIGNATURE:
            raise NotValidSignatureError
        position = archive.tell()
    return position


def read_source_name(archive_name, position):
    with open(archive_name, 'rb') as archive:
        archive.seek(position)
        name_len = int.from_bytes(archive.read(1), 'big')
        source_name = archive.read(name_len).decode()
        position = archive.tell()
    return position, source_name


class TooLongFilenameError(Exception):
    pass


class NotValidSignatureError(Exception):
    pass
