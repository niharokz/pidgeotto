#!/bin/python3

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 08-05-2021.
#       SOURCE [server.py] LAST MODIFIED ON 14-04-2025.
#

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from os import path, chdir
from yaml import safe_load
from rich import print
from rich.console import Console
import argparse
import sys

console = Console()

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/') or '.' not in self.path.split('/')[-1]:
            self.path += ".html"
        return super().do_GET()

def server(port=5555):
    try:
        # Load config.yml
        if not path.exists("config.yml"):
            console.print("[bold red]Error:[/bold red] config.yml not found in the current directory.")
            sys.exit(1)

        with open('config.yml', encoding="utf-8") as conf:
            config = safe_load(conf.read())

        home_path = config.get("home_path", "public")

        if not path.exists(home_path):
            console.print(f"[bold red]Error:[/bold red] The folder '{home_path}' does not exist. Try building the site first.")
            sys.exit(1)

        chdir(path.join(home_path))

        # Start server with custom handler
        httpd = TCPServer(("", port), CustomHandler)
        console.print(f"\n[bold green]✅ Pidgeotto server is live![/bold green]")
        console.print(f"📂 Serving directory: [cyan]{path.abspath(home_path)}[/cyan]")
        console.print(f"🌐 Access it on: [yellow]http://localhost:{port}[/yellow]")
        console.print("[dim]Press Ctrl+C to stop the server[/dim]")

        httpd.serve_forever()

    except KeyboardInterrupt:
        console.print("\n[bold red]✋ Server stopped.[/bold red]")
        httpd.server_close()

    except Exception as e:
        console.print("\n[bold red]❌ Oops! Something went wrong while serving the site.[/bold red]")
        console.print("[dim]Possible causes and suggestions:[/dim]")
        console.print(f"  1. [yellow]Not a valid Pidgeotto directory[/yellow] - Ensure you are in the correct directory where your site was generated.")
        console.print(f"  2. [yellow]Project not built yet[/yellow] - Make sure to run the build process before starting the server. You can use [bold]pidgey build[/bold] to generate the site.")
        console.print(f"\n[dim]Debug Info: {e}[/dim]")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a local server to serve your Pidgeotto site.")
    parser.add_argument("-p", "--port", type=int, default=5555, help="Port to run the server on (default: 5555)")
    args = parser.parse_args()

    server(args.port)


