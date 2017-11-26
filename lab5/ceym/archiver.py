import argparse


class CEYMArchiverUtility:
    def __init__(self, decompress_func, compress_func, show_func):
        self.decompress_func = decompress_func
        self.compress_func = compress_func
        self.show_func = show_func
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--unpack',
                            help='unpack archive to current folder')
        parser.add_argument('-p', '--pack',
                            help='pack <filename>.<ext> to <filename>.ceym')
        parser.add_argument('-n', '--name',
                            help='specify filename to `pack` or `unpack`')
        parser.add_argument('-s', '--show', help='show archive info')
        self.parser = parser

    def run(self):
        args = self.parser.parse_args()
        if args.unpack and args.pack:
            print('Choose only one of `pack` and `unpack`')
            exit(1)
        if args.show and args.name:
            print("You can't use `name` with `show` flag")
            exit(1)
        if args.unpack:
            self.decompress_func(args.unpack, args.name)
        if args.pack:
            self.compress_func(args.pack, args.name)
        if args.show:
            self.show_func(args.show)
