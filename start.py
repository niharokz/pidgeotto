from argparse import ArgumentParser
from sohoj import creator, builder, server, __version__


def main():

    parser = ArgumentParser(prog='rupantar', description='Easily configurable static website generator with a focus on minimalism.')
    parser.add_argument("-v", "--version", action="version", version="{version}".format(version=__version__) )
    subparsers = parser.add_subparsers(dest='type', help='command help', required=True)
    
    parser_init = subparsers.add_parser('init', help='start new pidgeotto').add_argument("name")
    parser_new = subparsers.add_parser('new', help='create new note/post/page').add_argument("name")
    parser_build = subparsers.add_parser('build', help='build the pidgeotto')
    parser_serve = subparsers.add_parser('serve', help='serve the pidgeotto')
    args = parser.parse_args()
    
    if args.type == "init" and args.name:
        creator.createPidgey(args.name)
    elif args.type == "new" and args.name:
        creator.createNote(args.name)
    elif args.type == 'build':
        builder.buildPidgey()
    elif args.type == 'serve':
        server.server()
    
    else: 
        parser.print_help()

# Entry point
if __name__ == '__main__':
    main()

