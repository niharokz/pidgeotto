#!/bin/python

#   
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nihar.page] ON 10-04-2021.
#       SOURCE [pidgey.py] LAST MODIFIED ON 20-04-2021.
#

# External imports
from pidgey import creator,builder,__version__
from argparse import ArgumentParser

    
def main():
    parser = ArgumentParser(prog='pidgey', description='Yet another simple static site generator.')
    parser.add_argument("-v", "--version", action="version", version="{version}".format(version=__version__) )
    subparsers = parser.add_subparsers(dest='type', help='command help', required=True)
    parser_init = subparsers.add_parser('init', help='start new pidgeotto').add_argument("name")
    parser_new = subparsers.add_parser('new', help='create new note/post/page').add_argument("name")
    parser_build = subparsers.add_parser('build', help='build the pidgeotto')
    args = parser.parse_args()
    if args.type == "init" and args.name:
        creator.createPidgey(args.name)
    elif args.type == "new" and args.name:
        creator.createNote(args.name)
    elif args.type == 'build':
        builder.buildPidgey()
    else: 
        parser.print_help()
