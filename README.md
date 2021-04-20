# NIHARS.COM: BACKEND AND TEMPLATE

## Description
This static webpage generator is to source https://nihars.com.

## Prerequisites
''' pip install pyyaml, jinja2, markdown2 '''
* PyYAML:	To consume the config file and header of blog posts.
* jinja2:	Templating engine
* markdown2:	To convert markdown to HTML

## Structure
* config.yml:	To configure the title, name, CSS file, js file, and other configurations.
* resource:	Location to store all CSS, js, image data.
* content:	All markdown files are stored here.
* layout:	Layouts for different HTML pages are kept here.
* nihars.py:	Main file. Programs start from here.
* gem.py: Main gemini file. Gemini capsules will be created from here.

## Usage:
* nihars.py: to publish all files inside a public directory
* gem.py: to publish all gemini capsules inside capsule directory
* create_note.py: to create a new post with name post
* server.py: to creata a local server at 0.0.0.0:8000
