# -*-coding: utf-8 -*-

"""This scripts generates a html page"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import string

from tornado.options import define, options
define("port", default=8800, help="run on the given port", type=int)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",MainHandler),
            (r"/submit/(\w*)",FormHandler),
        ]
        settings = {
            "template_path" : os.path.join(os.path.dirname(__file__), \
                "template"),
            "static_path" : os.path.join(os.path.dirname(__file__), "static"),
            "debug" : True,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("buyagrade.html")

class FormHandler(tornado.web.RequestHandler):
    def post(self, info):
        self.set_header("Content-Type", "text/html")
        name = self.get_argument("name",'')
        section = self.get_argument("section",'')
        crednum = self.get_argument("crednum",'')
        cretype = self.get_argument("cretype",'')
        infomation = {}
        infomation["name"] = name
        infomation["section"] = section
        infomation["crednum"] = crednum
        infomation["cretype"] = cretype
        if name == '' or section == '' or crednum == '' or cretype == '':
            self.render("error.html")
        elif (not self.isValid(crednum, cretype)):
            self.render("error.html")
        else:
            newcrednum = string.replace(infomation["crednum"], '-', '')
            infomation["crednum"] = newcrednum  
            self.writeToFile(infomation)
            content = self.readFromFile()
            self.render("confirm.html", info = infomation, text = content)

    def writeToFile(self, infomation):
        fw = file("./data/suckers.txt",'a')
        info = infomation["name"] + ';' + infomation["section"] + ';' + \
        infomation["crednum"] + ';' + infomation["cretype"] + '\n'
        fw.write(info)
        fw.close()
    def readFromFile(self):
        fr = file("./data/suckers.txt",'r')
        content = fr.readlines()
        return content

    def isValid(self, crednum, cretype):
        newcrednum = string.replace(crednum, '-', '')
        
        if (len(newcrednum) != 16):
            return False
        elif (cretype == 'visa' and newcrednum[0] != '4'):
            return False
        elif (cretype == 'mastercard' and newcrednum[0] != '5'):
            return False
        else:
            sumup = 0
            for i in range(len(newcrednum)):
                if i % 2 == 1:
                    sumup = sumup + int(newcrednum[i])
                else:
                    temp = 2 * int(newcrednum[i])
                    if temp < 10:
                        sumup = sumup + temp
                    else:
                        tenth = temp/10
                        single = temp % 10
                        sumup = sumup + tenth + single

            if sumup % 10 == 0:
                return True
            else:
                return False 







if __name__ == "__main__":
    tornado.options.parse_command_line()
    HTTPSERVER = tornado.httpserver.HTTPServer(Application())
    HTTPSERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
