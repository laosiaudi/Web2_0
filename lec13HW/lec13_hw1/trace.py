#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

import samples as gps
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('ajax.html')

class TaxiHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('position_mark_for_trace.html')
                
class TraceService(tornado.web.RequestHandler):
    def get(self):
        print "web service calling\n"
        taxi_id = self.get_argument("jsoncallback")
        gpslist = gps.read_trace_by_taxi_id(taxi_id)
        jsonlist = []
        for gpsdata in gpslist:
            jsonlist.append(gpsdata.__dict__)
        resp_string = json.dumps(jsonlist)
        self.write(resp_string)
		
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/hello", HelloHandler),
    (r"/taxi", TaxiHandler),
    (r"/taxi/services/trace", TraceService),
],debug=True)

if __name__ == "__main__":
    application.listen(8887)
    tornado.ioloop.IOLoop.instance().start()
    
