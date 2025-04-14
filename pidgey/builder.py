#!/bin/python

#   
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 10-04-2021.
#       SOURCE [builder.py] LAST MODIFIED ON 14-04-2025.
#

# External imports
from shutil import copytree, rmtree, copy
from os import path, makedirs, sep
from glob import glob
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown
from time import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def buildPidgey():
    start_time = time()
    total_notes = 0
    failed_notes = 0
    skipped_notes = []

    console.rule("[bold green]🔨 Starting Build Process")

    # Function to read markdown content from file
    def readmd(md):
        with open(md, 'r', encoding='utf8', errors='ignore') as data:
            return data.read()

    # Function to render and write a page
    def create_page(template, post_detail, md, filename):
        post_template = Environment(loader=FileSystemLoader(searchpath='./')).get_template(template)

        post_title = post_date = post_data = posts_list = last_date = nextpage = post_meta = post_subtitle = ""
        post_path = home_path

        # Decide filename and context based on whether it's index/rss or a note
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
            post_title = post_detail.get("title")
            post_subtitle = post_detail.get("subtitle")
            post_date = post_detail.get("date")
            post_meta = post_detail.get("meta")
            post_data = filename.split(sep)
            post_path = path.join(home_path)
            post_file = post_data[2].replace('.md', '.html')
            post_data = post_data[1]
            makedirs(post_path, exist_ok=True)

        # Render template and write to file
        with open(path.join(post_path, post_file), 'w', encoding='utf8', errors='ignore') as output_file:
            output_file.write(
                post_template.render(
                    title=title,
                    post_title=post_title,
                    post_subtitle=post_subtitle,
                    date=post_date,
                    metad=post_meta,
                    url=path.join(url, post_file),
                    article=markdown(md),
                    posts=posts_list,
                    home=home_md,
                    header=markdown(readmd(header_md)),
                    footer=markdown(readmd(footer_md)),
                    nextpage=nextpage,
                    last_date=last_date,
                    config=config
                )
            )

        return post_file

    # MAIN BUILD PROCESS
    try:
        with open('config.yml', encoding='utf8', errors='ignore') as conf:
            config = safe_load(conf.read())
            for key, val in config.items():
                globals()[key] = val

        # Validate essential config keys
        required_keys = ['home_path', 'resource_path', 'content_path', 'note_template', 'home_template', 'feed_template', 'home_md', 'header_md', 'footer_md', 'title', 'url']
        for key in required_keys:
            if key not in config:
                console.print(f"[bold red]❌ Missing config key:[/bold red] {key}")
                return

        # Reset output directory and copy static resources
        if path.exists(home_path):
            rmtree(home_path)
        copytree(resource_path, home_path)

        # Build each note
        posts = []
        for note_path in glob(path.join(content_path, "note", "*.md")):
            try:
                yaml_lines, ym, md = [], '', ''
                with open(note_path, encoding='utf8', errors='ignore') as infile:
                    for s in infile:
                        if s.startswith('---'):
                            for s in infile:
                                if s.startswith('---'):
                                    break
                                yaml_lines.append(s)
                            ym = ''.join(yaml_lines)
                            md = ''.join(infile)
                            break

                post_detail = safe_load(ym)
                if post_detail is not None:
                    post_url = create_page(note_template, post_detail, md, note_path)
                    ymd = post_detail
                    ymd.update({'url': '/' + post_url})
                    ymd.update({'note': markdown(md)})
                    posts.append(ymd)
                    total_notes += 1
                    console.print(f"[green]✔ Built:[/green] {post_url}")
                else:
                    skipped_notes.append(note_path)
                    console.print(f"[yellow]⚠️ Skipped:[/yellow] No frontmatter in {note_path}")
            except Exception as e:
                failed_notes += 1
                console.print(f"[red]❌ Error in:[/red] {note_path}")
                console.print_exception()

        # Sort posts by date (descending)
        posts = sorted(posts, key=lambda post: post.get('date', ''), reverse=True)

        # Build homepage and RSS
        create_page(home_template, None, readmd(home_md), "index.html")
        create_page(feed_template, None, readmd(home_md), "rss.xml")

        # Final summary
        console.rule("[bold cyan]✅ Build Summary")
        summary = Table(show_header=True, header_style="bold magenta")
        summary.add_column("Metric")
        summary.add_column("Count", justify="right")
        summary.add_row("Notes Processed", str(total_notes))
        summary.add_row("Skipped Notes", str(len(skipped_notes)))
        summary.add_row("Failed Notes", str(failed_notes))
        summary.add_row("Time Taken (s)", f"{(time() - start_time):.2f}")
        console.print(summary)

    except Exception as e:
        console.print(Panel("[bold red]Something went wrong while building your site![/bold red]\n\n[italic]Make sure you're inside a valid Pidgey directory.[/italic]", title="❌ Build Failed"))
        console.print_exception()
