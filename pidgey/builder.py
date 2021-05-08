#!/bin/python

#   
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nihar.page] ON 10-04-2021.
#       SOURCE [builder.py] LAST MODIFIED ON 08-05-2021.
#

# External imports
from shutil import copytree, rmtree, copy
from os import path, makedirs
from glob import glob
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

def buildPidgey():
    # Create Page
    def create_page(template,post_detail,md,filename):
        post_template = Environment(loader=FileSystemLoader(searchpath='./')).get_template(template)
        post_title = title
        post_date = post_data = posts_list = last_date = nextpage = post_meta = post_subtitle = ""
        post_path =  home_path
        if filename=="index.html":
            post_file = filename
            posts_list = posts
        elif filename.endswith(".xml") :
            post_file = filename
            posts_list = posts
            last_date = posts_list[0].get('date')
        elif post_detail == None :
            post_file = filename.replace('.md','.html')
        else:
            post_title = post_detail.get("title")
            post_subtitle = post_detail.get("subtitle")
            post_date = post_detail.get("date")
            post_meta = post_detail.get("meta")
            post_data = filename.split('/')
            post_path = path.join(home_path)
            post_file = post_data[2].replace('.md','.html')
            post_data = post_data[1]

            makedirs(post_path,exist_ok=True)

        with open(path.join(post_path,post_file),'w') as output_file:
            output_file.write(
                post_template.render(
                    title = title,
                    post_title = post_title,
                    post_subtitle = post_subtitle,
                    date = post_date,
                    metad = post_meta,
                    url = path.join(url,post_file),
                    article = markdown(md),
                    posts = posts_list,
                    home = home_md,
                    header = markdown(readmd(header_md)),
                    footer = markdown(readmd(footer_md)),
                    nextpage = nextpage,
                    last_date = last_date,
                    config=config
                )
            )
        output_file.close()
        return post_file
    
    
    # Markdown file to string
    def readmd(md):
        with open(md,'r') as data:
            return data.read()


    # PROGRAM STARTS HERE
    try:
        with open('config.yml') as conf:
            config = safe_load(conf.read())
            for key,val in config.items():
                globals()[key] = val

        # Recreated home path with resource
        if path.exists(home_path):
            rmtree(home_path)
        copytree(resource_path, home_path)
        
        #Create all pages from content/note
        posts = []
        for note in glob(path.join(content_path,"note","*.md")):
            yaml_lines, ym, md = [],'',''
            with open(note) as infile:
                for s in infile:
                    if s.startswith('---'):
                        for s in infile:
                            if s.startswith('---'):
                                break;
                            else:
                                yaml_lines.append(s)
                        ym = ''.join(yaml_lines)
                        md = ''.join(infile)
                        break;
            post_detail=safe_load(ym)
            if (post_detail is not None):
                post_url = create_page(note_template,post_detail,md,note)
                ymd = post_detail
                ymd.update({'url' : '/'+post_url})
                ymd.update({'note' : markdown(md)})
                posts += [ymd]
        
        #Sort posts based on date in descending order
        posts= sorted(posts, key=lambda post :  post['date'], reverse=True)
        
        # Other pages are created here
        create_page(home_template,None,readmd(home_md),"index.html")
        create_page(feed_template,None,readmd(home_md),"rss.xml")

    except:
        print("while building pidgey, some issue occured.")
        print("This can be due to \n\t1. Not a pidgey directory. \n\t2. Unknown file structure")


