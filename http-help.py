# a http server for help system
PORT = 8000
DOC_ROOT = 'public'



from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import json

import os.path
from urllib.parse import urlparse
import xml

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    #self.wfile.write(bytes("<html><body><h1>Hello World</h1></body></html>", "utf-8"))
    self.log_message("self.request=" + str(self.request))
    self.log_message("self.path=" + str(self.path))
    #self.log_message("self.client_address=" + str(self.client_address))
    #self.log_message("self.server=" + str(self.server))
    #print("dir(http)=" + str(dir("http")))
    act = None
    if(self.path.startswith("/rest/")):
      act = self.path[6:]
      if len(act) == 0:
        ret = {
          "search_target" : act,
          "type" : "",
          "dir" : dir(),
          "doc" : ""
        }
      else:
        ect = eval(act)
        #self.log_message(str(dir(act)))
        ret = {
          "search_target" : act,
          "type" : str(type(ect)),
          "dir" : dir(ect),
          "doc" : ect.__doc__
        }
      #self.wfile.write(bytes("<br><h1>dir(" + act + ")</h1>" + str(dir(ect)) + "", "utf-8"))
      #self.log_message(str(dir(act.__doc__)))
      #self.wfile.write(bytes("<br><h1>" + act + ".__doc__</h1><pre>" + str(ect.__doc__) + "</pre>", "utf-8"))
      #self.wfile.write(bytes("<br><h1>type(" + act + ")</h1><pre>" + str(type(ect)) + "</pre>", "utf-8"))
      self.request
      self.send_response(200)
      self.send_header('Content-type', 'application/json; charset=UTF-8')
      self.end_headers()
      self.wfile.write(bytes(json.dumps(ret, ensure_ascii=False, indent=2), "utf-8"))
    else:
      # /rest/ 以外
      #root
      if self.path == "" or self.path == "/":
          self.send_response(301)
          self.send_header('Content-type', 'text/html; charset=UTF-8')
          self.send_header('location', '/index.html')
          self.end_headers()
          self.log_message("redirect " + str(self.path))
      else:
        o = urlparse(self.path)
        opath = o.path
        if o.path[0] == "/":
          opath = o.path[1:]
        self.log_message("o=" + str(o))
        #self.path = self.path[1:]
        if(".." in opath):
          self.send_response(401)
          self.send_header('Content-type', 'text/html; charset=UTF-8')
          self.end_headers()
          self.log_message("ERROR path contains .. " + str(opath))
          self.wfile.write(bytes("<br><h1>path error (" + opath + ")</h1>", "utf-8"))
        else:
          fn = os.path.join(DOC_ROOT, opath)
          self.log_message("DOC_ROOT=" + DOC_ROOT + " fn=" + str(fn))
          try:
            with open(fn, "rb") as f:
              self.send_response(200)
              self.send_header('Content-type', 'text/html; charset=UTF-8')
              self.end_headers()
              self.wfile.write(f.read())
              #self.wfile.write(bytes("<script>target='" + self.path + "'", "utf-8"))
          except IOError:
              self.send_response(404)
              self.send_header('Content-type', 'text/html; charset=UTF-8')
              self.end_headers()

run(handler_class=MyHandler)