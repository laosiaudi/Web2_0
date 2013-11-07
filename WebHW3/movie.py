# -*-coding: utf-8 -*-

"""This scripts generates a html page"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import sys
import multiprocessing

from tornado.options import define, options
define("port", default=9990, help="run on the given port", type=int)


class movie:
    def __init__(self, info, overview, alist, pic):
        self.infolist = []
        self.reviewgroupl = []
        self.reviewgroupr = []
        self.overview = {}
        self.pic = pic
        for line in info:
            self.infolist.append(line)
        for lint in overview:
            info = lint.split(':')
            self.overview[info[0]] = info[1]
        for i in range(len(alist)):
            if i < len(alist)/2:
                content = []
                for line in alist[i]:
                    line = line[:-1]
                    content.append(line)

                self.reviewgroupl.append(content)
            else:
                content = []
                for line in alist[i]:
                    line = line[:-1]
                    content.append(line)
                self.reviewgroupr.append(content)
            

        


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\w*)",MainHandler),
        ]
        settings = {
            "template_path" : os.path.join(os.path.dirname(__file__), \
                "template"),
            "static_path" : os.path.join(os.path.dirname(__file__), "static"),
            "debug" : True,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self,input):
        if input == '':
            self.write('<h1>Welcome!</h1>')
        else:
            dire = './'
            infopath = '/info.txt'
            overviewpath = '/generaloverview.txt'
            allpath_info = dire + input + infopath
            allpath_over = dire + input + overviewpath
            filetoken_info = open(allpath_info,'r')
            filetoken_over = open(allpath_over,'r')
            review = []
            filename = ['/review1.txt', '/review2.txt', '/review3.txt', \
            '/review4.txt', '/review5.txt', '/review6.txt', \
            '/review7.txt', '/review8.txt', '/review9.txt', \
            '/review10.txt', '/review11.txt', '/review12.txt']
            files = os.listdir(dire + input)
            num = len(files)

            for i in range(num - 4):
                filenames = dire + input + filename[i]
                ftoken = open(filenames,'r')
                review.append(ftoken)
            

            pic = input + '.png'
            objectm = movie(filetoken_info, filetoken_over, review, pic)


            self.render("template.html", movie = objectm)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    HTTPSERVER = tornado.httpserver.HTTPServer(Application())    
    HTTPSERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
