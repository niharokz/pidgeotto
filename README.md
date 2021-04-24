# pidgeotto

## Description
Yet another static website generator. 

Why choose pidgeotto?
1. Free of javascript.
2. Extensible, flexible, forkable.
3. Minimal and fast.
4. Free under MIT License.

## Installation
``` pip install pidgeotto ```

$ pip install git+https://github.com/niharokz/pidgeotto

## Prerequisites
By default, pidgeotto will install the below packages from PyPI pip
``` pyyaml, jinja2, markdown2 ```
* PyYAML:	To consume the config file and header of blog posts.
* jinja2:	Templating engine
* markdown2:	To convert markdown to HTML

## Usage:
```console
$ pidgey init project
```
To initiate pidgeotto with name "project"

```console
$ pidgey new pageName
```
To create new page/post/note with name "pageName"

```console
$ pidgey build pageName
```
To build static pages and keep those in the "public" directory.

## Extra Functionalaties
1. showInHome tag is present in each note markdown.
        ``` showInHome: True ``` 
        will create page which are blog/note post.
        
        ``` showInHome: False ``` 
        will create page which are pages.

2. config.yml is extensible. 
        For example, if you want to add favicon.ico. Keep favicon in the resource folder.
        ``` favicon: resource/favicon.ico ``` 
        in config.yml
        In template, add {{ config.get('favicon') }}.

3. Extra metadata per page.
        If you want to add some metadata to your page, it can be done using the below command on the markdown page.
        ``` meta : '<link rel="stylesheet" type="text/css" href="/extra.css" /> ```


## Structure

    pidgeotto_project
    ├── public
    ├── config.yml
    ├── content
    │   ├── header.md
    │   ├── footer.md
    │   ├── home.md
    │   ├── archive.md
    │   └── note
    │       └── other_pages.md
    ├── resource
    └── templates
        ├── home_template.html
        ├── note_template.html
        └── rss_template.xml

* config.yml:	To configure the title, name, CSS file, js file, and other configurations.
* resource:	Location to store all CSS, js, image data and other static content.
* content:	All markdown files are stored here.
* template:	Layouts for different HTML pages are kept here.
* public: All generated static files. It can be changed in config.yml

## Example

Below are examples of sites running via pidgeotto.
1. [nihar.page](https://nihar.page)


## TODO

* (A) 24-04-2021 Add Serve functionality
* (B) 24-04-2021 Clean up some clutter coding

## Update

### 0.0.3

* Removed archived page
* MIT Licensed
* showInHome only True or False
* RSS Template fixed
