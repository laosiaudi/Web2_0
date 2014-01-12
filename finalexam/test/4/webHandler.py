#coding=utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import json
import codecs
codecs.register(lambda name: name == 'cp65001' and codecs.lookup('utf-8') or None)

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
class quesion:
    def __init__(self,title,content,tag,date):
        self.title = title
        self.content = content
        self.tag = tag
        self.date = date

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/index", MainHandler),
                    (r"/tag", TagHandler)]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
        )
        conn = pymongo.Connection("localhost",27017)
        finaldb = conn["Web2_0FinalTestDB"]
        self.db = finaldb["problemSets"]
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        database = self.application.db
        questionlist = []

        for qset in database.find():
            title = qset['title']
            date = qset['post_date']
            content = qset['content']
            taglist = []
            for item in qset['tags']:
                taglist.append(item)
            newq = quesion(title,content,taglist,date)
            questionlist.append(newq)

        self.render('index.html',qset = questionlist)

    def post(self):
        pass    


class TagHandler(tornado.web.RequestHandler):
    def post(self):
        match = self.get_argument("search")
        database = self.application.db
        questionlist = []

        for qset in database.find():
            title = qset['title']
            date = qset['post_date']
            content = qset['content']
            taglist = []
            for item in qset['tags']:
                if item == match:
                    tempset = {}
                    tempset["title"] = title
                    tempset["post_date"] = date
                    tempset["content"] = content
                    tempset["tags"] = qset["tags"]
                    questionlist.append(tempset)
        qulist = json.dumps(questionlist)
        self.write(qulist)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
