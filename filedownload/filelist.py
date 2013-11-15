import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define,options
define("port",default=8886,help="run on the given port",type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",MainHandler),
            (r"/(\w*).mp3",DownloadHandler),
        ]
        settings = {
            
            "static_path" : os.path.join(os.path.dirname(__file__), "static"),
            "debug" : True,
        }
        tornado.web.Application.__init__(self, handlers, **settings)
class DownloadHandler(tornado.web.RequestHandler):
    def get(self,ingo):
        
        filename = "static/songs/" + ingo + ".mp3"
        f =open(filename)
        
        self.set_header("Content-Disposition","attachment") 
        self.set_header("Content-Type","application/mp3")
       
        f.close()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	filenames = os.listdir('./static/songs/')
    	i = 0
    	
    	"""for n in xrange(0, len(filenames)):
            filenames[n] = filenames[n] + "   " + str(os.path.getsize(filenames[n])) + "k"""
        #self.set_header("Content-Disposition","attachment") 
        self.render("template.html", title="My folder", items=filenames)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    #app=tornado.web.Application(handlers=[(r"/",MainHandler),(r"/static/(.*)",tornado.web.StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__), "static")))],debug=True)
    #app = tornado.web.Application(handlers=[(r"/",MainHandler)],static_path=os.path.join(os.path.dirname(__file__), "static"))
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
