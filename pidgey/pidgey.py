#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 14-04-2025
#       SOURCE [pidgey.py] LAST MODIFIED ON 14-04-2025.
#
from argparse import ArgumentParser
from pidgey import __version__, creator, builder, server
from rich.console import Console
from rich.prompt import Prompt
from os import path

console = Console()

# Function to print success, error, and info messages using rich
def print_success(message):
    console.print(message, style="bold green")

def print_error(message):
    console.print(message, style="bold red")

def print_info(message):
    console.print(message, style="yellow")

def main():
    parser = ArgumentParser(prog='pidgey', description='A simple static site generator for your blog or personal website.')
    parser.add_argument("-v", "--version", action="version", version=f"v{__version__}")
    
    subparsers = parser.add_subparsers(dest='type', help='Command help', required=True)
    
    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize a new Pidgeotto project.')
    parser_init.add_argument("name", help="The name of your project directory.")
    
    # New command (simplified, no type flag)
    parser_new = subparsers.add_parser('new', help='Create a new note or post.')
    parser_new.add_argument("name", help="Enter the name for your new note/post.")

    # Build command
    parser_build = subparsers.add_parser('build', help='Build the Pidgeotto site.')

    # Serve command
    parser_serve = subparsers.add_parser('serve', help='Serve your site locally.')

    args = parser.parse_args()
    
    if args.type == "init" and args.name:
        try:
            print_info(f"Initializing your Pidgeotto project... {args.name} 🎉")
            creator.createPidgey(args.name)
            print_success(f"Your project '{args.name}' has been successfully initialized! Let's start creating content.")
        except Exception as e:
            print_error(f"Oops! Something went wrong while initializing your project. Error: {e}")
    
    elif args.type == "new" and args.name:
        try:
            # Check if the note/post already exists
            if path.exists(args.name):
                # Ask user if they want to overwrite
                overwrite = Prompt.ask(f"The file '{args.name}' already exists. Do you want to overwrite it?", choices=["y", "n"], default="n")
                if overwrite.lower() == "n":
                    print_info(f"Cancelled creating the note/post '{args.name}'.")
                    return
            
            print_info(f"Creating a new note/post with the name '{args.name}'...")
            creator.createNote(args.name)
            print_success(f"Your note/post '{args.name}' was successfully created! Time to add some content to it.")
        except Exception as e:
            print_error(f"Uh-oh! There was an issue creating your note/post. Error: {e}")
        
    elif args.type == 'build':
        try:
            print_info("Building your static site. Please wait while we generate the pages...")
            builder.buildPidgey()
            print_success("Your site has been successfully built! You can now check it out.")
        except Exception as e:
            print_error(f"Something went wrong while building your site. Error: {e}")
    
    elif args.type == 'serve':
        try:
            print_info("Starting the server to serve your site locally...")
            server.server()  # Assuming server.py handles the rest
            print_success("Your site is now being served locally! Visit the URL to preview.")
        except Exception as e:
            print_error(f"Error while serving your site. Please try again. Error: {e}")
    
    else:
        print_error("Oops! It seems like you entered an invalid command or missing arguments.")
        parser.print_help()

if __name__ == "__main__":
    main()
