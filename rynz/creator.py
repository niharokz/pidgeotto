#!/bin/python3

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 18-04-2021.
#       SOURCE [creator.py] LAST MODIFIED ON 15-04-2025.
#

from os import mkdir, path, makedirs
from datetime import datetime
import sys
from rich.console import Console

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
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{current_time}] {message}"
    console.print(message, style=styles.get(style, "yellow"))


def get_input(prompt, default_value, validator=None):
    """
    Prompts user for input with an optional default and validator.

    Args:
        prompt (str): The input prompt.
        default_value (str): Default input value if the user provides none.
        validator (callable): A function to validate input (optional).

    Returns:
        str: The validated user input.
    """
    while True:
        user_input = input(prompt).strip() or default_value
        if validator and not validator(user_input):
            print_message(
                "Invalid input. Please try again.", "error", timestamp=True
            )
        else:
            return user_input


def is_valid_url(url):
    """
    Checks if the given string contains a basic valid domain structure.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    return "." in url


def safe_create_directory(directory):
    """
    Safely creates a directory if it doesn't already exist.

    Args:
        directory (str): Path to the directory to create.

    Exits:
        On failure to create the directory.
    """
    try:
        if not path.exists(directory):
            makedirs(directory)
            print_message(
                f"Created directory: {directory}", "success", timestamp=True
            )
        else:
            print_message(
                f"Directory already exists: {directory}", "info", timestamp=True
            )
    except Exception as e:
        print_message(
            f"❌ Error creating directory {directory}: {e}", "error", timestamp=True
        )
        sys.exit(1)


def createConfig(rynzName):
    """
    Creates the default configuration file `config.yml`.

    Args:
        rynzName (str): The name of the project directory.
    """
    try:
        with open(path.join(rynzName, 'config.yml'), 'w') as f:
            title = rynzName
            url = 'yourdomain.tld'

            conf_data = f"""
# Mandatory Configuration
title: {title}
url: {url}
note_template: template/note_template.html
home_template: template/home_template.html
feed_template: template/feed_template.xml
home_path: public
content_path: content
resource_path: static
home_md: content/home.md
header_md: content/header.md
footer_md: content/footer.md

# Optional Configuration
site-title: {title}
css: demo.css
desc: Write anything that human and machine can understand.
mail: some@mail.com
"""
            f.write(conf_data)
            print_message("config.yml created.", "success", timestamp=True)
    except Exception as e:
        print_message(
            f"❌ Error creating config.yml: {e}", "error", timestamp=True
        )


def createTemplate(rynzName, template_type, file_content):
    """
    Creates a template file with the provided content.

    Args:
        rynzName (str): The name of the project directory.
        template_type (str): The name of the template file.
        file_content (str): The content to write to the template file.
    """
    try:
        template_file_path = path.join(rynzName, 'template', template_type)
        with open(template_file_path, 'w') as f:
            f.write(file_content)
            print_message(
                f"{template_type} created.", "success", timestamp=True
            )
    except Exception as e:
        print_message(
            f"❌ Error creating {template_type}: {e}", "error", timestamp=True
        )

# Template: Home Page
home_template_content = """
<!DOCTYPE html>
<html lang="en-IN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content=" {{ config.get('desc') }} ">
<title>{{ config.get('site-title') }}</title>
<link rel="stylesheet" href="{{ config.get('css') }}">
<link rel="alternate" type="application/atom+xml" title="Recent blog posts" href="/rss.xml">
</head>
<body>
<header>
<h1><a href="/">{{ title | lower }}</a></h1>
{{ header }}
</header>
<section>
{{ article }}
<ul>
{% for post in posts %}
  {% if "note" in post.tags %}
    <li>{{ post.date.strftime('%d %m %Y') }} ; <a href="{{ post.url }}">{{ post.title | lower }}</a></li>
  {% endif %}
{% endfor %}
{% if nextpage %} <a href="{{ nextpage }}">Older Notes >> </a> {% endif %}
</ul>
</section>
<footer>
{{ footer }}
</footer>
</body>
</html>
"""

# Template: Note Page
note_template_content = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>{{ post_title }}</title>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content=" {{ post_subtitle }} ">
<link rel="stylesheet" href="{{ config.get('css') }}">
<link rel="alternate" type="application/atom+xml" title="Recent blog posts" href="/rss.xml">
</head>
<body>
<header>
<h1>{{ post_title }}</h1>
</header>
<article>
{{ article }}
{% if date %}
<p># Last updated on <time>{{ date.strftime('%d %b %Y') }}.</time></p>
{% endif %}
</article>
<footer>
{{ footer }}
</footer>
</body>
</html>
"""

# Template: Feed (RSS)
feed_template_content = """
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{{ title }}</title>
    <atom:link href="{{ url }}" rel="self" type="application/rss+xml" />
    <link>{{ url }}</link>
    <description>{{ subtitle }}</description>
    <lastBuildDate>{{ last_date.strftime('%a, %d %b %Y %H:%M:%S GMT') }}</lastBuildDate>
    <language>en-IN</language>
    <image>
      <url>{{ config.get('url') }}/{{ config.get('pht') }}</url>
      <title>{{ title }}</title>
      <link>{{ url }}</link>
      <width>32</width>
      <height>32</height>
    </image>
    {% for post in posts %}
        {% if "note" in post.tags %}
            <item>
            <title>{{ post.title }}</title>
            <link>{{ config.get('url') }}{{ post.url }}</link>
            <pubDate>{{ post.date.strftime('%a, %d %b %Y %H:%M:%S GMT') }}</pubDate>
            <guid isPermaLink="false">{{ config.get('url') }}{{ post.url }}</guid>
            <description><![CDATA[{{ post.subtitle }} - {{ post.note }} ]]></description>
            </item>
        {% endif %}
    {% endfor %}
  </channel>
</rss>
"""

# Create content/header/footer/note   
def createContent(rynzName):
    """
    Creates initial content, including `header.md`, `footer.md`, and `home.md`.

    Args:
        rynzName (str): The name of the project directory.
    """
    try:
        safe_create_directory(path.join(rynzName, 'content', 'note'))

        with open(path.join(rynzName, 'content', 'header.md'), 'w') as f:
            f.write(
                "*   [Home](/)\n*   [Other Links](/)\n"
                "*   [Edit content/header.md](/)"
            )
            print_message("header.md created.", "success", timestamp=True)

        with open(path.join(rynzName, 'content', 'footer.md'), 'w') as f:
            f.write(
                "*   [Home](/)\n*   [RSS](/)\n"
                "*   [Edit content/footer.md](/)\n"
                "*   powered by [Rynz](https://rynz.de)"
            )
            print_message("footer.md created.", "success", timestamp=True)

        with open(path.join(rynzName, 'content', 'home.md'), 'w') as f:
            f.write(
                "Welcome to Rynz.\nThis is a sample homepage which can be "
                "edited at /content/home.md"
            )
            print_message("home.md created.", "success", timestamp=True)

        # Ensure the note directory exists before calling createNote
        note_dir = path.join(rynzName, 'content', 'note')
        safe_create_directory(note_dir)

        # Generate a sample note
        createNote("notepage1.md", rynzName)

    except Exception as e:
        print_message(f"❌ Error creating content: {e}", "error", timestamp=True)
        

def createNote(noteName, rynzName=''):
    """
    Creates a markdown note file with sample content.

    Args:
        noteName (str): Name of the note file to create.
        rynzName (str): Parent directory for the note file. Defaults to ''.
    """
    try:
        note_dir = path.join(rynzName, 'content', 'note')

        # Ensure the directory exists
        if not path.exists(note_dir):
            makedirs(note_dir)

        if not noteName.lower().endswith('.md'):
            noteName += '.md'

        with open(path.join(note_dir, noteName), 'w') as f:
            conf_data = (
                """---
title: "Sample Note Page."
subtitle: "Sample subtitle"
date: {t}
tags: [note,generic]
---

# This is a sample note page which can be edited/renamed at /content/note/{noteName}
# This is heading 1

## This is heading 2

### This is heading 3

#### This is heading 4

##### This is heading 5

###### This is heading 6

**Bold**

*italic*

* list
* list

1. ordered list
2. ordered list

[link](/)

Sample paragraph is written like this with lorem ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

            """).format(t=datetime.now().strftime("%Y-%m-%d"), noteName=noteName)

            f.write(conf_data)
            print_message(
                f"{noteName} is created at {path.join(note_dir, noteName)}",
                "success",
                timestamp=True
            )

    except Exception as e:
        print_message(
            f"While generating page {noteName}, some issue occurred: {e}",
            "error",
            timestamp=True
        )


def createRynz(rynzName):
    """
    Initializes a Rynz project with all necessary directories and files.

    Args:
        rynzName (str): The name of the project directory.
    """
    try:
        safe_create_directory(rynzName)
        safe_create_directory(path.join(rynzName, 'template'))
        safe_create_directory(path.join(rynzName, 'static'))
        safe_create_directory(path.join(rynzName, 'content'))
        safe_create_directory(path.join(rynzName, 'content', 'note'))

        createConfig(rynzName)
        createTemplate(rynzName, 'home_template.html', home_template_content)
        createTemplate(rynzName, 'note_template.html', note_template_content)
        createTemplate(rynzName, 'feed_template.xml', feed_template_content)
        createContent(rynzName)

        print_message(
            f"Rynz project {rynzName} created successfully!", "success",
            timestamp=True
        )

    except Exception as e:
        print_message(
            f"❌ Error creating Rynz project {rynzName}: {e}", "error",
            timestamp=True
        )
        sys.exit(1)
