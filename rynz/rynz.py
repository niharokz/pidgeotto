#!/bin/python

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 28-04-2025
#       SOURCE [rynz.py] LAST MODIFIED ON 28-04-2025.
#

"""
Main entry point for the Rynz static site generator.

This script handles the command-line interface (CLI) for the Rynz package, allowing users to:
- Create new projects.
- Add new pages.
- Deploy the site.
- Serve the site locally.
- Edit configuration.
- Run tests.
- Save changes using Git.
"""

from argparse import ArgumentParser
from . import __version__, creator, builder, manage
from rich.console import Console
from rich.prompt import Prompt
from os import path
import sys

# Initialize the rich console for printing styled messages
console = Console()

def print_message(message, style="info"):
    """
    Prints a styled message using the Rich console.

    Args:
        message (str): The message to display.
        style (str): Message style ("success", "error", or "info").
    """
    styles = {
        "success": "bold green",
        "error": "bold red",
        "info": "yellow"
    }
    console.print(message, style=styles.get(style, "yellow"))

def main():
    """
    Main function that handles the CLI commands for the Rynz project.

    Supports the following commands:
    - create: Initialize a new Rynz project.
    - add: Add a new Markdown note or blog post.
    - deploy: Convert Markdown files to static HTML.
    - serve: Serve the site locally.
    - config: View or edit the config.yml file.
    - test: Run tests on the project setup.
    - save: Save changes with Git.
    """
    # Set up the argument parser
    parser = ArgumentParser(
        prog='rynz',
        description='🕊️ Rynz: Really Your Note Zenerator.'
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"Rynz v{__version__}"
    )

    # Define subcommands
    subparsers = parser.add_subparsers(dest='type', help='Available commands')
    subparsers.required = True

    # create -- initialize rynz project
    parser_create = subparsers.add_parser('create', help='Create a new Rynz project.')
    parser_create.add_argument(
        "name", help="Name of your project directory"
    )

    # add -- add new pages to rynz project
    parser_add = subparsers.add_parser('add', help='Create a new note or blog post.')
    parser_add.add_argument(
        "name", help="Filename for your new Markdown note/post"
    )

    # deploy -- Publishes the rynz project
    subparsers.add_parser(
        'deploy', help='Convert Markdown files into static HTML'
    )

    # serve -- run the rynz project locally
    subparsers.add_parser(
        'serve', help='Serve your site locally at http://localhost:5555'
    )

    # config -- edit the config yaml in rynz project
    subparsers.add_parser(
        'config', help='View or edit site configuration (config.yml)'
    )

    # test -- test the project locally
    subparsers.add_parser(
        'test', help='Test your Rynz setup and structure'
    )

    # save -- stage and commit changes
    parser_save = subparsers.add_parser(
        'save', help='Save changes with Git (stage and commit)'
    )
    parser_save.add_argument(
        "-m", "--message", type=str,
        default="Changes saved via rynz save",
        help="Commit message for the save operation"
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Handle each command based on user input
        if args.type == "create" and args.name:
            print_message(
                f"📁 Creating project: {args.name}", "info"
            )
            try:
                creator.createRynz(args.name)
                print_message(
                    f"✅ Project '{args.name}' created! Start writing in `content/note/`.",
                    "success"
                )
            except FileNotFoundError:
                print_message(
                    f"❌ Failed to create project '{args.name}'. Directory not found.",
                    "error"
                )
            except PermissionError:
                print_message(
                    f"❌ Permission denied while creating project '{args.name}'.",
                    "error"
                )
            except Exception as e:
                print_message(
                    f"🔥 An error occurred: {e}", "error"
                )
            sys.exit(0)

        elif args.type == "add" and args.name:
            if path.exists(args.name):
                overwrite = Prompt.ask(
                    f"⚠️ The file '{args.name}' already exists. Overwrite?",
                    choices=["y", "n"], default="n"
                )
                if overwrite.lower() != "y":
                    print_message(
                        "⛔ Note creation cancelled.", "info"
                    )
                    sys.exit(0)
            print_message(
                f"📝 Adding new note: {args.name}", "info"
            )
            try:
                creator.createNote(args.name)
                print_message(
                    f"✅ Note '{args.name}' created successfully.", "success"
                )
            except Exception as e:
                print_message(
                    f"🔥 An error occurred while adding the note: {e}", "error"
                )
            sys.exit(0)

        elif args.type == 'deploy':
            print_message(
                "🔧 Building your static site...", "info"
            )
            try:
                builder.buildRynz()
                print_message(
                    "✅ Site deployment completed!", "success"
                )
            except Exception as e:
                print_message(
                    f"🔥 An error occurred while deploying the site: {e}", "error"
                )
            sys.exit(0)

        elif args.type == 'serve':
            print_message(
                "🚀 Serving site locally at http://localhost:5555 ...", "info"
            )
            try:
                manage.server()
            except Exception as e:
                print_message(
                    f"🔥 An error occurred while serving the site: {e}", "error"
                )
            sys.exit(0)

        elif args.type == 'config':
            print_message(
                "⚙️ Viewing or editing config.yml...", "info"
            )
            try:
                manage.manage_config()
            except Exception as e:
                print_message(
                    f"🔥 An error occurred while managing the configuration: {e}", "error"
                )
            sys.exit(0)

        elif args.type == 'test':
            print_message(
                "⚙️ Running tests...", "info"
            )
            try:
                manage.run_tests()
                print_message(
                    "✅ All tests passed successfully.", "success"
                )
            except Exception as e:
                print_message(
                    f"🔥 An error occurred while running tests: {e}", "error"
                )
            sys.exit(0)

        elif args.type == 'save':
            print_message(
                "💾 Saving changes to Git repository...", "info"
            )
            try:
                manage.save_changes(args.message)
            except Exception as e:
                print_message(
                    f"🔥 An error occurred while saving changes: {e}", "error"
                )
            sys.exit(0)

        else:
            print_message(
                "❌ Invalid command or missing arguments. Use `rynz --help`.", "error"
            )
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print_message(
            f"🔥 An unexpected error occurred: {e}", "error"
        )
        sys.exit(1)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()