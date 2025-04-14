# Pidgeotto

## Description
Pidgeotto is a minimal, fast, and JavaScript-free static site generator — built for developers who love Markdown, speed, and simplicity.

### Why choose Pidgeotto?
1. No JavaScript by default.
2. Clean, forkable Python code.
3. Flexible templating with Jinja2.
4. Fast, Markdown-first workflow.
5. Fully open-source under the MIT License.

## Installation
```
pip install pidgeotto
```

Or install the latest version directly from GitHub:
```
pip install git+https://github.com/niharokz/pidgeotto
```

## Prerequisites
Pidgeotto installs the following dependencies automatically:
- `pyyaml` — for configuration files and frontmatter parsing
- `jinja2` — templating engine
- `markdown2` — for Markdown to HTML conversion
- `rich` — for better CLI display (colorful output)

## Basic Usage

### 1. Initialize a new site
```
pidgey init project
```
Creates the required folder structure and template files under `project/`.

### 2. Create a new note/page
```
pidgey new pageName
```
Generates a new Markdown file under `content/note/pageName.md`.

### 3. Build the site
```
pidgey build
```
Renders all markdown into HTML and places them under the `public/` directory.

### 4. Serve the site locally
```
pidgey serve
```
Launches a local server on http://localhost:5555

Serve on a custom port:
```
pidgey serve -port 2222
```

## Extra Features

### 1. Page Visibility on Homepage
Each note can control visibility on the homepage with:
```
showInHome: true    # default, shown on home page
showInHome: false   # hidden from home page, useful for static pages like "About"
```

### 2. Extend config.yml with custom keys
You can extend `config.yml` to include custom fields like favicon:
```
favicon: resource/favicon.ico
```
Use it in your HTML template:
```
{{ config.get('favicon') }}
```

### 3. Custom Metadata in Notes
Add metadata per note:
```
meta: '<link rel="stylesheet" href="/extra.css">'
```
Use it in your HTML template:
```
{{ meta }}
```

## Folder Structure

```lua
pidgeotto_project/
|-- public/
|-- config.yml
|-- content/
|   |-- header.md
|   |-- footer.md
|   |-- home.md
|   `-- note/
|       `-- sample.md
|-- resource/
|   `-- style.css
`-- templates/
    |-- home_template.html
    |-- note_template.html
    `-- rss_template.xml

```

- `config.yml`: site-wide configuration (title, paths, theme, etc.)
- `resource/`: static assets like CSS, images, and favicon
- `content/`: Markdown content (header, footer, notes)
- `templates/`: Jinja2 templates for rendering HTML
- `public/`: generated output folder (can be changed in config)

## Example
Visit a live site generated using Pidgeotto:  
[https://nih.ar](https://nih.ar)

## Changelog

### v1.0.0 – Stable Release
- Pretty URLs supported (/note/a/index.html)
- Custom ports for dev server (pidgey serve -port 2222)
- Server auto-handles /abc → /abc.html
- Skips notes with missing frontmatter
- Homepage listing respects `showInHome`
- Global error handling improvements
- Color-coded CLI output with Rich
- Windows compatibility
- Markdown metadata injection via meta tag
- Improved project structure and modular codebase

## License
MIT License