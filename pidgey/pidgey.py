#!/bin/python

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 14-04-2025
#       SOURCE [pidgey.py] LAST MODIFIED ON 25-04-2025.
#

from argparse import ArgumentParser
from pidgey import __version__, creator, builder, server
from rich.console import Console
from rich.prompt import Prompt
from os import path
import sys

console = Console()

def print_success(message):
    console.print(message, style="bold green")

def print_error(message):
    console.print(message, style="bold red")

def print_info(message):
    console.print(message, style="yellow")

def main():
    parser = ArgumentParser(
        prog='pidgey',
        description='🕊️ Pidgeotto: A minimal, Markdown-first static site generator.'
    )
    parser.add_argument("-v", "--version", action="version", version=f"Pidgeotto v{__version__}")

    subparsers = parser.add_subparsers(dest='type', help='Available commands', required=True)

    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize a new Pidgeotto project.')
    parser_init.add_argument("name", help="Name of your project directory")

    # New command
    parser_new = subparsers.add_parser('new', help='Create a new note or blog post.')
    parser_new.add_argument("name", help="Filename for your new Markdown note/post")

    # Build command
    subparsers.add_parser('build', help='Convert Markdown files into static HTML')

    # Serve command
    subparsers.add_parser('serve', help='Serve your site locally at http://localhost:5555')

    args = parser.parse_args()

    try:
        if args.type == "init" and args.name:
            print_info(f"📁 Initializing project: {args.name}")
            creator.createPidgey(args.name)
            print_success(f"✅ Project '{args.name}' created! Start writing in `content/note/`.")
            sys.exit(0)

        elif args.type == "new" and args.name:
            if path.exists(args.name):
                overwrite = Prompt.ask(
                    f"⚠️ The file '{args.name}' already exists. Overwrite?",
                    choices=["y", "n"], default="n"
                )
                if overwrite.lower() != "y":
                    print_info("⛔ Note creation cancelled.")
                    sys.exit(0)

            print_info(f"📝 Creating new note: {args.name}")
            creator.createNote(args.name)
            print_success(f"✅ Note '{args.name}' created successfully.")
            sys.exit(0)

        elif args.type == 'build':
            print_info("🔧 Building your static site...")
            builder.buildPidgey()
            print_success("✅ Site build complete! Check the `public/` folder.")
            sys.exit(0)

        elif args.type == 'serve':
            print_info("🚀 Serving site locally at http://localhost:5555 ...")
            server.server()
            sys.exit(0)

        else:
            print_error("❌ Invalid command or missing arguments.")
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print_error(f"🔥 An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
