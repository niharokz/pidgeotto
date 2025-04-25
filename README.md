
# Pidgeotto

## Description
Pidgeotto is a minimal, fast, and JavaScript-free static site generator designed for developers who love Markdown, speed, and simplicity.

### Why Choose Pidgeotto?
- No JavaScript by default.
- Clean, forkable Python code.
- Flexible templating with Jinja2.
- Fast, Markdown-first workflow.
- Fully open-source under the MIT License.

## Installation
You can install Pidgeotto using `pip`:

```bash
pip install pidgeotto
```

Or install the latest version directly from GitHub:

```bash
pip install git+https://github.com/niharokz/pidgeotto
```

### Dependencies
Pidgeotto automatically installs the following dependencies:
- `pyyaml`: for configuration files and frontmatter parsing
- `jinja2`: templating engine
- `markdown2`: for converting Markdown to HTML
- `rich`: for improved CLI display (colorful output)

## Basic Usage

### 1. Initialize a New Site
```bash
pidgey init project
```
This creates the required folder structure and template files under `project/`.

### 2. Create a New Note/Page
```bash
pidgey new pageName
```
Generates a new Markdown file under `content/note/pageName.md`.

### 3. Build the Site
```bash
pidgey build
```
Renders all Markdown files into HTML and places them in the `public/` directory.

### 4. Serve the Site Locally
```bash
pidgey serve
```
Launches a local server at [http://localhost:5555](http://localhost:5555).

Serve on a custom port:
```bash
pidgey serve -p 2222
```

## Extra Features

### 1. Page Visibility on Homepage (Using Tags)
Instead of using `showInHome`, page visibility is now controlled via tags. To control whether a post appears on the homepage:

- Add the `home` tag to the post.

Example:

```markdown
tags: [home]
```

Make sure your template is set up to filter and display pages with this tag.

### 2. Extend `config.yml` with Custom Keys
You can extend `config.yml` to include custom fields like favicon:

```yaml
favicon: resource/favicon.ico
```

Use this value in your HTML template:

```html
<link rel="icon" href="{{ config.get('favicon') }}" />
```

### 3. Custom Metadata in Notes
Add metadata per note:

```yaml
meta: '<link rel="stylesheet" href="/extra.css">'
```

Use it in your HTML template:

```html
{{ meta }}
```

## Folder Structure

```bash
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

### Folder Breakdown:
- `config.yml`: Site-wide configuration (title, paths, theme, etc.)
- `resource/`: Static assets like CSS, images, and favicon.
- `content/`: Markdown content (header, footer, and notes).
- `templates/`: Jinja2 templates for rendering HTML.
- `public/`: Generated output folder (this is where the built site will reside).

## Example
Visit a live site generated using Pidgeotto:  
[https://nih.ar](https://nih.ar)

## Changelog

### v1.0.0 : Major Release
- Replaced `showInHome` with a tag-based system to control page visibility on the homepage.
- Rich error handling improvements, including enhanced error display with color coding.
- Enhanced error handling in CLI commands, providing more detailed feedback.
- Improved project structure and code modularity.
- Various performance optimizations and bug fixes.

### v0.9.9 : Beta Release
- Custom ports for dev server (`pidgey serve -p 2222`).
- Server auto-handles `/abc` → `/abc.html`.
- Skips notes with missing frontmatter.
- Homepage listing respects `showInHome`.
- Global error handling improvements.
- Color-coded CLI output with Rich.
- Windows compatibility.
- Markdown metadata injection via meta tag.
- Improved project structure and modular codebase.

## License
MIT License
