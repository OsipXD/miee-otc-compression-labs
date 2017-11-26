#!/usr/bin/env python
from ceym.archiver import CEYMArchiverUtility
from arithmetic import pack, unpack
from ceym.format import check_signature, read_source_name


def show(archive_name):
    try:
        position = check_signature(archive_name)
    except NotValidSignatureError:
        print('Not valid ceym archive.')
        return
    _, source_name = read_source_name(archive_name, position)
    print('Valid ceym archive with "{0}" file.'.format(source_name))


if __name__ == '__main__':
    archiver = CEYMArchiverUtility(pack, unpack, show)
    archiver.run()
