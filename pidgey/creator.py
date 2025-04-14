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

# Enhanced logging function with timestamp
def log_message(message, level="info"):
    levels = {"info": "[INFO]", "success": "[SUCCESS]", "error": "[ERROR]"}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} {levels.get(level, '[INFO]')} {message}")

# User input helper with optional validation
def get_input(prompt, default_value, validator=None):
    while True:
        user_input = input(prompt).strip() or default_value
        if validator and not validator(user_input):
            log_message("Invalid input. Please try again.", "error")
        else:
            return user_input

def is_valid_url(url):
    return "." in url  # Very basic domain check

def safe_create_directory(directory):
    try:
        if not path.exists(directory):
            makedirs(directory)
            log_message(f"Created directory: {directory}", "success")
        else:
            log_message(f"Directory already exists: {directory}", "info")
    except Exception as e:
        log_message(f"Error creating directory {directory}: {e}", "error")
        sys.exit(1)

# Create config.yml
def createConfig(pidgeyName):
    try:
        with open(path.join(pidgeyName, 'config.yml'), 'w') as f:
            title = pidgeyName
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
            log_message("config.yml created.", "success")
    except Exception as e:
        log_message(f"Error creating config.yml: {e}", "error")

# Template creators
def createTemplate(pidgeyName, template_type, file_content):
    try:
        template_file_path = path.join(pidgeyName, 'template', template_type)
        with open(template_file_path, 'w') as f:
            f.write(file_content)
            log_message(f"{template_type} created.", "success")
    except Exception as e:
        log_message(f"Error creating {template_type}: {e}", "error")

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
  {% if (post.showInHome is undefined) or post.showInHome %}
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
      {% if (post.showInHome is undefined) or post.showInHome %}
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
def createContent(pidgeyName):
    try:
        safe_create_directory(path.join(pidgeyName, 'content', 'note'))

        with open(path.join(pidgeyName, 'content', 'header.md'), 'w') as f:
            f.write("*   [Home](/)\n*   [Other Links](/)\n*   [Edit content/header.md](/)")
            log_message("header.md created.", "success")

        with open(path.join(pidgeyName, 'content', 'footer.md'), 'w') as f:
            f.write("*   [Home](/)\n*   [RSS](/)\n*   [Edit content/footer.md](/)\n*   powered by [Pidgeotto](/)")
            log_message("footer.md created.", "success")

        with open(path.join(pidgeyName, 'content', 'home.md'), 'w') as f:
            f.write("Welcome to Pidgeotto.\nThis is a sample homepage which can be edited at /content/home.md")
            log_message("home.md created.", "success")

        # Ensure the note directory exists before calling createNote
        note_dir = path.join(pidgeyName, 'content', 'note')
        safe_create_directory(note_dir)

        # Now using the createNote function to generate a sample note
        createNote("notepage1.md",pidgeyName)

    except Exception as e:
        log_message(f"Error creating content: {e}", "error")

# Create a note
def createNote(noteName,pidgeyName='', showInHome=True):
    try:
        note_dir = path.join(pidgeyName, 'content', 'note')
        
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
showInHome: {s}
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
                """).format(t=datetime.now().strftime("%Y-%m-%d"), s=showInHome, noteName=noteName)

            f.write(conf_data)
            print(f"{noteName} is created at {path.join(note_dir, noteName)}")

    except Exception as e:
        print(f"While generating page {noteName}, some issue occurred: {e}")

# Main initializer
def createPidgey(pidgeyName):
    try:
        safe_create_directory(pidgeyName)
        safe_create_directory(path.join(pidgeyName, 'template'))
        safe_create_directory(path.join(pidgeyName, 'static'))
        safe_create_directory(path.join(pidgeyName, 'content'))
        safe_create_directory(path.join(pidgeyName, 'content', 'note'))

        createConfig(pidgeyName)
        createTemplate(pidgeyName, 'home_template.html', home_template_content)
        createTemplate(pidgeyName, 'note_template.html', note_template_content)
        createTemplate(pidgeyName, 'feed_template.xml', feed_template_content)
        createContent(pidgeyName)

        log_message(f"Pidgey project {pidgeyName} created successfully!", "success")

    except Exception as e:
        log_message(f"Error creating Pidgey project {pidgeyName}: {e}", "error")
        sys.exit(1)
