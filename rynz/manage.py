#!/bin/python3

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 08-05-2021.
#       SOURCE [manage.py] LAST MODIFIED ON 28-04-2025.
#

from os import path, chdir
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import sys
import yaml
import argparse
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

# Initialize console for colorful output
console = Console()

def print_message(message, style="info", timestamp=False):
    """
    Prints a styled message using the Rich console.

    Args:
        message (str): The message to display.
        style (str): Message style ("success", "error", or "info").
        timestamp (bool): Whether to include a timestamp in the message.
    """
    styles = {
        "success": "bold green",
        "error": "bold red",
        "info": "yellow"
    }
    if timestamp:
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{current_time}] {message}"
    console.print(message, style=styles.get(style, "yellow"))


# Mandatory configuration keys
MANDATORY_CONFIG_KEYS = [
    "title", "url", "note_template", "home_template", "feed_template",
    "home_path", "content_path", "resource_path", "home_md", "header_md",
    "footer_md"
]

def run_tests():
    """
    Run tests to validate the configuration file and key project elements.
    Ensures all mandatory keys are present, the syntax of config.yml is correct,
    and key project components (home_path, index.html, deployment directory) exist and are valid.

    Exits:
        On validation failure.
    """
    # Load and validate config.yml syntax
    try:
        config = load_config()
    except yaml.YAMLError as e:
        print_message(f"❌ Error: YAML syntax issue in config.yml: {e}", "error", timestamp=True)
        sys.exit(1)
    except Exception as e:
        print_message(f"❌ Error: Unable to load config.yml: {e}", "error", timestamp=True)
        sys.exit(1)

    print_message("✅ config.yml loaded successfully.", "success", timestamp=True)

    # Check for mandatory keys in config.yml
    missing_keys = [key for key in MANDATORY_CONFIG_KEYS if key not in config]
    if missing_keys:
        print_message("❌ Error: Missing mandatory keys in config.yml:", "error")
        for key in missing_keys:
            print_message(f" - {key}", "error")
        sys.exit(1)
    print_message("✅ All mandatory keys are present in config.yml.", "success", timestamp=True)

    # Validate home_path exists
    home_path = config.get("home_path", "public")
    if not path.exists(home_path):
        print_message(f"❌ Error: The specified home_path '{home_path}' does not exist.", "error", timestamp=True)
        sys.exit(1)
    print_message(f"✅ home_path '{home_path}' exists.", "success", timestamp=True)

    # Check if index.html exists in home_path
    index_file = path.join(home_path, "index.html")
    if not path.exists(index_file):
        print_message(f"❌ Error: index.html is missing in '{home_path}'.", "error", timestamp=True)
        sys.exit(1)
    print_message(f"✅ index.html exists in '{home_path}'.", "success", timestamp=True)

    # Validate index.html file content (basic validation)
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "<!DOCTYPE html>" not in content or "<title>" not in content:
                print_message("❌ Error: index.html is not properly formatted.", "error", timestamp=True)
                sys.exit(1)
            print_message("✅ index.html is properly formatted.", "success", timestamp=True)
    except Exception as e:
        print_message(f"❌ Error: Unable to read index.html. Reason: {e}", "error", timestamp=True)
        sys.exit(1)

    # Validate deployment directory exists
    public_dir = config.get("home_path", "public")
    if not path.exists(public_dir):
        print_message(f"❌ Error: Deployment directory '{public_dir}' does not exist.", "error", timestamp=True)
        sys.exit(1)
    print_message(f"✅ Deployment directory '{public_dir}' exists.", "success", timestamp=True)

    print_message("✅ All tests passed successfully.", "success", timestamp=True)

def load_config():
    """Load the configuration from config.yml."""
    if not path.exists("config.yml"):
        print_message("❌ Error: config.yml not found.", "error", timestamp=True)
        sys.exit(1)

    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config):
    """Save the updated configuration to config.yml."""
    with open("config.yml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print_message("✅ Config saved successfully!", "success", timestamp=True)


def display_config(config):
    """Display current configuration."""
    table = Table(title="Current Configuration")

    for key, value in config.items():
        table.add_row(key, str(value))

    console.print(table)

def add_key(config):
    """
    Adds a new key-value pair to the configuration.

    Args:
        config (dict): Current configuration dictionary.
    """
    new_key = Prompt.ask("Enter the name of the new key").strip()
    if new_key in config:
        print_message(f"⚠️ Key '{new_key}' already exists in the configuration.", "info")
        return
    new_value = Prompt.ask(f"Enter the value for '{new_key}'").strip()
    config[new_key] = new_value
    save_config(config)
    print_message(f"✅ Added key '{new_key}' with value '{new_value}' to the configuration.", "success")

def modify_key(config):
    """
    Modifies the value of an existing key in the configuration.

    Args:
        config (dict): Current configuration dictionary.
    """
    key_to_modify = Prompt.ask("Enter the name of the key to modify").strip()
    if key_to_modify not in config:
        print_message(f"❌ Key '{key_to_modify}' does not exist in the configuration.", "error")
        return
    new_value = Prompt.ask(f"Enter the new value for '{key_to_modify}'").strip()
    config[key_to_modify] = new_value
    save_config(config)
    print_message(f"✅ Modified key '{key_to_modify}' with new value '{new_value}'.", "success")

def delete_key(config):
    """
    Deletes a key-value pair from the configuration.

    Args:
        config (dict): Current configuration dictionary.
    """
    key_to_delete = Prompt.ask("Enter the name of the key to delete").strip()
    if key_to_delete not in config:
        print_message(f"❌ Key '{key_to_delete}' does not exist in the configuration.", "error")
        return
    del config[key_to_delete]
    save_config(config)
    print_message(f"✅ Deleted key '{key_to_delete}' from the configuration.", "success")

def manage_config():
    """Interactively manage the configuration."""
    config = load_config()
    while True:
        print_message("\nCurrent Configuration:\n", "info")
        display_config(config)

        action = Prompt.ask(
            "\nWhat would you like to do?",
            choices=["view", "add", "modify", "delete", "exit"],
            default="view",
        )

        if action == "view":
            display_config(config)
        elif action == "add":
            add_key(config)
        elif action == "modify":
            modify_key(config)
        elif action == "delete":
            delete_key(config)
        elif action == "exit":
            print_message("Exiting config manager...", "info", timestamp=True)
            break


def server(port=5555):
    """Start the local HTTP server."""
    try:
        config = load_config()
        home_path = config.get("home_path", "public")

        if not path.exists(home_path):
            print_message(
                f"❌ Error: '{home_path}' does not exist.", "error", timestamp=True
            )
            sys.exit(1)

        chdir(path.join(home_path))

        httpd = TCPServer(("", port), SimpleHTTPRequestHandler)
        print_message(
            f"✅ Server is live! at http://localhost:{port}", "success",
            timestamp=True
        )
        httpd.serve_forever()

    except KeyboardInterrupt:
        print_message("✋ Server stopped.", "error", timestamp=True)
    except Exception as e:
        print_message(f"❌ Error: {e}", "error", timestamp=True)
        sys.exit(1)


def save_changes(commit_message="Changes saved via rynz save"):
    """
    Automates Git workflow: stage and commit changes.

    Args:
        commit_message (str): Commit message for the changes.

    Returns:
        None
    """
    try:
        # Check if it's a valid Git repository
        if not path.exists(".git"):
            print_message("❌ Error: Not a Git repository. Please initialize Git first.", "error", timestamp=True)
            return

        # Stage changes
        subprocess.run(["git", "add", "."], check=True)
        print_message("✅ All changes staged for commit.", "success", timestamp=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print_message(f"✅ Changes committed with message: '{commit_message}'", "success", timestamp=True)

    except subprocess.CalledProcessError as e:
        print_message(f"❌ Error during Git operation: {e}", "error", timestamp=True)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Rynz server.")
    parser.add_argument(
        "-p", "--port", type=int, default=5555,
        help="Port to run the server on."
    )
    args = parser.parse_args()

    run_tests()
    manage_config()
    server(args.port)