#-*- coding:utf-8 -*-
# AUTHOR:   apple
# FILE:     main.py
# 2013 @laosiaudi All rights reserved
# CREATED:  2013-12-26 14:22:30
# MODIFIED: 2013-12-26 15:48:11

import os
import tornado.ioloop
import tornado.web
import pymongo
import tornado.httpserver
import json
class BlogClass():
    def __init__(self,title,detail,content):
        self.title = title
        self.detail = detail
        self.content = content

class MainHandler(tornado.web.RequestHandler):
    def get(self):
      dbbase = self.application.db
      record = dbbase.find_one()
      title = record["title"]
      detail = record["detail"]
      content = record["content"]
      blog = BlogClass(title,detail,content)
      self.render('blog.html',blog=blog)
class AjaxService(tornado.web.RequestHandler):
    def get(self):
        db = self.application.db.find_one();
        commentdict = db["comment"];
        commentlist = json.dumps(commentdict);
        self.write(commentlist)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/",MainHandler),
        (r"/comment",AjaxService),
        ]
        settings = {"static_path":os.path.join(os.path.dirname(__file__),"static"),
                "template_path":os.path.join(os.path.dirname(__file__),"templates"),
                "debug":True
        }
        conn = pymongo.Connection("localhost",27017)
        self.db = conn.paperDB.infoDB
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
    HTTPSERVER = tornado.httpserver.HTTPServer(Application())
    HTTPSERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


