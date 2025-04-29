#!/bin/python

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 28-04-2025
#       SOURCE [builder.py] LAST MODIFIED ON 28-04-2025.
#

from shutil import copytree, rmtree
from os import path, makedirs, sep
from glob import glob
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown
from time import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize console for colorful output
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

def buildRynz():
    """
    Builds the static site by converting Markdown notes into HTML pages,
    using Jinja2 templates and configuration from config.yml.
    """
    start_time = time()
    total_notes = 0
    failed_notes = 0
    skipped_notes = []

    console.rule("[bold green]🔨 Starting Build Process")
    
    def readmd(filepath):
        """
        Reads and returns the raw content of a markdown file.

        Args:
            filepath (str): Path to the markdown file.

        Returns:
            str: File content as a string.
        """
        try:
            with open(filepath, 'r', encoding='utf8', errors='ignore') as data:
                return data.read()
        except Exception as e:
            print_message(f"❌ Error reading {filepath}: {e}", "error")
            return ""


    def create_page(template, post_detail, md_content, filename):
        """
        Renders and writes a page from a Jinja2 template and given content.
        Handles both single notes and special pages like index.html and RSS feeds.

        Args:
            template (str): Template filename.
            post_detail (dict): Frontmatter details for the post.
            md_content (str): Markdown content to render.
            filename (str): Output filename.

        Returns:
            str: Rendered file name or an empty string in case of error.
        """
        
        try:
            env = Environment(loader=FileSystemLoader(searchpath='./'))
            template_obj = env.get_template(template)

            # Initialize variables
            post_title = ""
            post_subtitle = ""
            post_date = ""
            post_meta = ""
            posts_list = ""
            last_date = ""
            post_data = filename.split(sep)
            post_path = home_path
			
            # Determine post details based on the filename
            if filename == "index.html":
                post_file = filename
                posts_list = posts
            elif filename.endswith(".xml"):
                post_file = filename
                posts_list = posts
                last_date = posts_list[0].get('date')
            elif post_detail is None:
                post_file = filename.replace('.md', '.html')
            else:
                post_title = post_detail.get("title", "")
                post_subtitle = post_detail.get("subtitle", "")
                post_date = post_detail.get("date", "")
                post_meta = post_detail.get("meta", "")
                post_data = filename.split(sep)
                post_path = path.join(home_path)
                post_file = post_data[2].replace('.md', '.html')
                post_data = post_data[1]
                makedirs(post_path, exist_ok=True)

            output_filepath = path.join(post_path, post_file)
            with open(output_filepath, 'w', encoding='utf8', errors='ignore') as output_file:
                output_file.write(
                    template_obj.render(
                        title=title,
                        post_title=post_title,
                        post_subtitle=post_subtitle,
                        date=post_date,
                        metad=post_meta,
                        url=path.join(url, post_file),
                        article=markdown(md_content),
                        posts=posts_list,
                        home=home_md,
                        header=markdown(readmd(header_md)),
                        footer=markdown(readmd(footer_md)),
                        last_date=last_date,
                        config=config
                    )
                )
            return post_file
        except Exception as e:
            print_message(f"❌ Error creating page {filename}: {e}", "error")
            return ""
    
    try:
        # Load configuration
        with open('config.yml', encoding='utf8', errors='ignore') as conf_file:
            config = safe_load(conf_file.read())

        # Set config values as globals
        for key, val in config.items():
            globals()[key] = val

        # Ensure all required configuration keys are present
        required_keys = [
            'home_path', 'resource_path', 'content_path', 'note_template',
            'home_template', 'feed_template', 'home_md', 'header_md',
            'footer_md', 'title', 'url'
        ]
        for key in required_keys:
            if key not in config:
                print_message(f"❌ Missing config key: {key}", "error")
                return

        # Reset output directory
        if path.exists(home_path):
            rmtree(home_path)
        copytree(resource_path, home_path)

        posts = []

        # Process each note
        for note_path in glob(path.join(content_path, "note", "*.md")):
            try:
                yaml_lines = []
                frontmatter, markdown_content = '', ''

                # Read frontmatter and body
                with open(note_path, encoding='utf8', errors='ignore') as infile:
                    for line in infile:
                        if line.startswith('---'):
                            for line in infile:
                                if line.startswith('---'):
                                    break
                                yaml_lines.append(line)
                            frontmatter = ''.join(yaml_lines)
                            markdown_content = ''.join(infile)
                            break

                post_detail = safe_load(frontmatter)

                if post_detail is not None:
                    # Build the note page
                    post_url = create_page(
                        note_template, post_detail, markdown_content, note_path
                    )

                    # Add to posts list for homepage/rss
                    post_entry = post_detail
                    post_entry.update({'url': '/' + post_url})
                    post_entry.update({'note': markdown(markdown_content)})
                    posts.append(post_entry)

                    total_notes += 1
                    print_message(f"✔ Built: {post_url}", "success")
                else:
                    # If no valid frontmatter found
                    skipped_notes.append(note_path)
                    print_message(f"⚠️ Skipped: No frontmatter in {note_path}", "info")
            except Exception:
                failed_notes += 1
                print_message(f"❌ Error in: {note_path}", "error")
                console.print_exception()

        # Sort posts by latest date
        posts = sorted(posts, key=lambda post: post.get('date', ''), reverse=True)

        # Build index.html and RSS feed
        create_page(home_template, None, readmd(home_md), "index.html")
        create_page(feed_template, None, readmd(home_md), "rss.xml")

        # Build summary table
        console.rule("[bold cyan]✅ Build Summary")
        summary = Table(show_header=True, header_style="bold magenta")
        summary.add_column("Metric")
        summary.add_column("Count", justify="right")
        summary.add_row("Notes Processed", str(total_notes))
        summary.add_row("Skipped Notes", str(len(skipped_notes)))
        summary.add_row("Failed Notes", str(failed_notes))
        summary.add_row("Time Taken (s)", f"{(time() - start_time):.2f}")
        console.print(summary)

    except Exception:
        console.print(Panel(
            "[bold red]Something went wrong while building your site![/bold red]\n\n"
            "[italic]Make sure you're inside a valid Rynz directory.[/italic]",
            title="❌ Build Failed"
        ))
        console.print_exception()