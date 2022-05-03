# a http server for help system
PORT = 8000
DOC_ROOT = 'public'



from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import inspect
import json

import os.path
import re
from urllib.parse import urlparse
import xml
import pydoc
import sys
from io import TextIOWrapper, BytesIO
import importlib

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    #self.wfile.write(bytes("<html><body><h1>Hello World</h1></body></html>", "utf-8"))
    #self.log_message("self.request=" + str(self.request))
    #self.log_message("self.path=" + str(self.path))
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
        ect = None
        try:
          ect = eval(act)
        except:
          #eval("" + act + " = importlib.importlib.import_module('" + act + "')")
          #importlib.import_module(act)
          #act0 = act.split(".")[0]
          #globals().update({act0:sys.modules[act0]})
          #ect = eval(act)
          self.safeImport(act)
        #self.log_message("ect=" + str((ect)))
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
    elif(self.path.startswith("/module/list")):
      self.send_response(200)
      self.send_header('Content-type', 'application/json; charset=UTF-8')
      self.end_headers()
      # see https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-into-some-sort-of-string-buffer/19345047#19345047
      # setup the environment
      #old_stdout = sys.stdout
      #sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
      # do something that writes to stdout or stdout.buffer
      #pydoc.help.listmodules()
      # get output
      #sys.stdout.seek(0)      # jump to the start
      #out = sys.stdout.read() # read output
      # restore stdout
      #sys.stdout.close()
      #sys.stdout = old_stdout
      #out = re.sub("(?s)^.*?\n\n", "", out)  # remove the first line
      #out = re.sub("(?s)\n\n.*?$", "", out) # remove the last line
      #outlist = re.split("W+|\s+|\n+", out) # split by whitespace
      #outlist = [x for x in outlist if x != ""] # remove empty strings
      #outlist = list(filter(None, outlist))  # remove empty strings another way
      #outlist.sort()
      #outlist = filter(lambda x: inspect.ismodule(x[1]), sys.modules.items())
      outlist = {
        "builtin" : {},
        "ondisk" : {}
      }
      for i in sys.modules.items():
        if "(built-in)" in str(i[1]):
          outlist["builtin"][i[0]] = str(i[1])
        else:
          outlist["ondisk"][i[0]] = str(i[1])
      ret = {
        #"modulelist" : list(map(lambda x:x[0], outlist))
        "builtin" : outlist["builtin"],
        "ondisk" : outlist["ondisk"]
      }
      self.wfile.write(bytes(json.dumps(ret, ensure_ascii=False, indent=2), "utf-8"))
    else:
      # redirect / to index.html
      if self.path == "" or self.path == "/":
          self.send_response(301)
          #self.send_response(200)
          self.send_header('Content-type', 'text/html; charset=UTF-8')
          self.send_header('location', '/modulelist.html')
          self.end_headers()
          self.log_message("redirect " + str(self.path))
          #self.wfile.write(bytes("<br><pre>" + help("modules") + ")</pre>", "utf-8"))
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
  def safeImport(self, mod):
    if mod != "":
      try:
        self.log_message("try import " + str(mod))
        #globals().update({mod:sys.modules[mod]})
        globals().update({mod:importlib.import_module(mod)})
        o = eval(mod)
      except:
        #self.safeImport(re.sub("\..*?$", "", mod))
        self.safeImport(re.sub("(.*)(\..+?)$", "\\1", mod))
        self.log_message("try again import " + str(mod))
        try:
          #globals().update({mod:sys.modules[mod]})
          globals().update({mod:importlib.import_module(mod)})
        except:
          self.log_error("try again import " + str(mod) + " failed")
          pass


run(handler_class=MyHandler)