from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from os import path, chdir
from yaml import safe_load


def server():
    try:
        with open('config.yml') as conf:
            config = safe_load(conf.read())
            for key,val in config.items():
                globals()[key] = val
        PORT = 5555
        chdir(path.join(home_path))
        httpd = TCPServer(("", PORT), SimpleHTTPRequestHandler)
        print("serving at port", PORT)
        httpd.serve_forever()
    except KeyboardInterrupt: 
        pass; 
        httpd.server_close() 
    except:
        print("while serving pidgey, some issue occured.")
        print("This can be due to \n\t1. Not a pidgey directory. \n\t2. Pidgey not built yet.")
