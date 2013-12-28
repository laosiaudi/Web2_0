#-*- coding:utf-8 -*-
# AUTHOR:   apple
# FILE:     main.py
# 2013 @laosiaudi All rights reserved
# CREATED:  2013-12-26 14:22:30
# MODIFIED: 2013-12-28 11:56:54

import os
import tornado.ioloop
import tornado.web
import pymongo
import tornado.httpserver
import json
import time
class BaseHandler(tornado.web.RequestHandler):
    """
    Implements basic handler
    """
    def get_current_user(self):
        return self.get_secure_cookie("user")
class BlogClass():
    def __init__(self,image,age,friends,email,name):
        self.image = image
        self.age = age
        self.friends = friends
        self.email = email
        self.name = name
class MainHandler(BaseHandler):
    def process(self,twlist,username):
        newlist = []
        for item in twlist:
            item["username"] = username
            newlist.append(item)
        return newlist
        
    def get(self, username):
      if self.current_user == '':
          self.redirect("/login")
      dbbase = self.application.db
      usr = self.current_user
      record = dbbase.find_one({"name":username})
      image = record["image"]
      email = record["email"]
      friends = record["friends"]
      age = record["age"]
      selftwitter = record["twitters"]
      ownlist = self.process(selftwitter,username)
      biglist = []
      for item in ownlist:
          biglist.append(item)
      for user in friends:
          newrc =  dbbase.find_one({"name":user})
          templist = self.process(newrc["twitters"],user)
          for item in templist:
              biglist.append(item)
      commentlist = sorted(biglist,key = lambda item:item["time"])
      blog = BlogClass(image,age,friends,email,username)
      self.render('blog.html',blog=blog,commentlist = commentlist)
class AjaxService(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument("username",'')
        content = self.get_argument("content",'')
        db = self.application.db.find_one({"name":username});
        newlist = db["twitters"];
        temp = dict()
        flag = True
        for item in newlist:
            if item["content"] == content:
                flag = False
                temp = item
                break
        if flag == False: 
            if temp != None and temp.has_key("comments"):
                commentdict = temp["comments"]
                commentlist = json.dumps(commentdict);
            else:
                commentlist = ''
        else:
            commentlist = ''
        self.write(commentlist)

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user != '':
            self.redirect("/" + "twitter/" + self.current_user)
        else:
            self.write('<html><body><form action="/login" method="post">'
                    'Name: <input type="text" name="name"/>'
                    'Password: <input type="text" name="pass"/>'
                    '<input type="submit" value="Sign in"/>'
                    '</form></body></html>')
    def post(self):
        usr = self.get_argument("name",'')
        password = self.get_argument("pass",'')
        '''
        to do here login
        '''
        dbbase = self.application.db.find_one({"name":usr})
        if dbbase == None:
            self.redirect("/login")
        else:
            if usr != '' and password != '' and password == dbbase["password"]:
                self.set_secure_cookie("user",usr)
                make_url = "/twitter/" + usr
                self.redirect(make_url)
            else:
                self.redirect("/login")
class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user",'')
        self.redirect("/login")

class NewCommentHandler(BaseHandler):
    def post(self):
        month = ['Jan','Feb','March','April','May','June','July','Aug','Sep','Oct','Nov','Dec']
        newComment = self.get_argument("newcomment",'')
        usr = self.current_user
        username = self.get_argument("username",'')
        content = self.get_argument("content",'')
        dbbase = self.application.db.find_one({"name":username})
        content = content.replace('&amp;','&')
        blog = dbbase["twitters"]
        newtime = time.strftime('%m %d %Y %H:%M:%S',time.localtime(time.time()))
        newdate = newtime.split(' ')
        newmonth = month[int(newdate[0])-1]
        newtime = newmonth
        for item in range(1,len(newdate)):
            newtime = newtime + ' ' + newdate[item]
        
        tempdic = []
        tdic = dict()
        index = 0
        newlistt = []
        newdic = dict()
        newdic["comment_date"] = newtime
        newdic["comment_by"] = usr
        newdic["comment_content"] = newComment
        for item in blog:
            if item["content"] == content:
                if item.has_key("comments"):
                    tempdic = item["comments"]
                    tempdic.append(newdic)
                    item["comments"] = tempdic
                else:
                    tempdic = []
                    tempdic.append(newdic)
                    item["comments"] = tempdic
                index += 1
                newlistt.append(item)
            else:
                newlistt.append(item)
        self.application.db.update({"name":username},{'$set':{"twitters":newlistt}},True)
        
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/comment",AjaxService),
        (r"/login",LoginHandler),
        (r"/logout",LogoutHandler),
        (r"/twitter/(\w+)",MainHandler),
        (r"/commit",NewCommentHandler)
        ]
        settings = {"static_path":os.path.join(os.path.dirname(__file__),"static"),
                "template_path":os.path.join(os.path.dirname(__file__),"templates"),
                "debug":True,
                "cookie_secret" :"61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        }
        conn = pymongo.Connection("localhost",27017)
        self.db = conn.twitterDB.userSets
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
    HTTPSERVER = tornado.httpserver.HTTPServer(Application())
    HTTPSERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


