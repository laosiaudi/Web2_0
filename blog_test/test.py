# -*-coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import time
import os
import pymongo
import tornado.httpserver
class BaseHandler(tornado.web.RequestHandler):
    """
    Implements basic handler
    """
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    """
    Implements main handler
    """
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("hello! " + name)

class LogoutHandler(BaseHandler):
    """
    Implements logout function
    """
    def get(self):
        self.set_secure_cookie("user",'')
        self.redirect("/login")
class LoginHandler(BaseHandler):
    """
    Implements log in function
    """
    data = {}
    flag = False
    def readuserinfo(self):
        fr = open('./data/users.txt','r')
        infomation = fr.readlines()
        for line in infomation:
            match = line[:-1].split(',')
            self.data[match[0]] = match[1]
        fr.close()
    def get(self):
        if self.current_user != '':
            self.redirect("/" + self.current_user + "/Charles/1")
        else:
            self.write('<html><body><form action="/login" method="post">'
                    'Name: <input type="text" name="name">'
                    'Password: <input type="text" name="pass">'
                    '<input type="submit" value="Sign in">'
                    '</form><form action="/register" method = "post">'
                    'Name:<input type="text" name="name">'
                    'Password: <input type="text" name="pass">'
                    '<input type = "submit" value="register">'
                    '</form></body></html>')
    def post(self):
        #self.readuserinfo()
        usr = self.get_argument("name",'')
        password = self.get_argument("pass",'')
        authdb = self.application.db.auth
        flag = authdb.find_one({"user":usr})
        if flag == None:
            self.render('http://thebest404pageever.com/')
        if usr != '' and password != '' and password == flag["passw"]:
            self.set_secure_cookie("user",usr)
            make_url = "/" + usr + "/Charles/1"
            self.redirect(make_url)
        else:
            self.redirect("/login")
class RegisterHandler(BaseHandler):
    def post(self):
        user = self.get_argument("name",'')
        passw = self.get_argument("pass",'')
        tempdic = dict()
        tempdic["user"] = user
        flag = self.application.db.auth.find_one(tempdic)
        if flag == None:
            tempdic["passw"] = passw
            self.application.db.auth.insert(tempdic)
            self.redirect("/login")
        else:
            self.write("<html><body>The username has already existed!</body></html>")

class BlogHandler(BaseHandler):
    """
    Implements basic handler
    """
    flag = False
    user = []
    def get(self,author_name):
        #self.readuserinfo()
        tempdb = self.application.db.auth
        tempflag = tempdb.find_one({"user":author_name})
        if tempflag == None: 
            self.redirect('http://thebest404pageever.com/')
        fr = open('./data/blog.txt','r')
        infomation = fr.readlines()
        tem = []
        for i in range(3):
            info = infomation[i]
            match = info[:-1].split(':')
            tem.append(match[1])
        fr.close()
        if self.current_user:
            self.flag = True
        comment = []
        """fr = open('./data/comments.txt','r')
        infomation = fr.readlines()
        for line in infomation:
            sth = line[:-1].split('|')
            item = []
            item.append(sth[0])
            item.append(sth[1])
            item.append(sth[2])
            comment.append(item)
            tempdic = {}
            tempdic["user"] = sth[0]
            tempdic["content"] = sth[2]
            tempdic["time"] = sth[1]
            commentdb.insert(tempdic)

        fr.close()"""
        commentdb = self.application.db.comment
        for item in commentdb.find():
            templist = []
            templist.append(item["user"])
            templist.append(item["time"])
            templist.append(item["content"])
            comment.append(templist)

        if author_name != self.current_user:
            self.flag = False
        self.render('./template.html', passtitle = tem[0], \
         author = tem[1], blog = tem[2] , comment = comment,flag = self.flag)
    def post(self,info):
        fw = open('./data/comments.txt','a')
        new_comment = self.get_argument("comment_submit")
        usr = self.current_user
        newtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        fw.write(usr+"|" + newtime + "|" + new_comment.encode('utf-8') + "\n")
        fw.close()
        commentdb = self.application.db.comment
        tempdic = {}
        tempdic["user"] = usr
        tempdic["content"] = new_comment.encode('utf-8')
        tempdic["time"] = newtime
        commentdb.insert(tempdic)
        new_url="/" + usr + "/Charles/1"
        self.redirect(new_url)

class AjaxService(BaseHandler):
    def post(self):
        content = self.get_argument("comment_submit")
        usr = self.current_user;
        newtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        addHtml = '<div class="comment"><p><span>' + usr + '</span>' + '  ' + newtime + '</p><p>&nbsp;&nbsp;&nbsp;&nbsp;' + content + '</p></div>'
        commentdb = self.application.db.comment
        tempdic = {}
        tempdic["content"] = content.encode('utf-8')
        tempdic["time"] = newtime
        tempdic["user"] = usr
        commentdb.insert(tempdic)
        self.write(addHtml)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/",MainHandler),
        (r"/some",AjaxService),
        (r"/login",LoginHandler),
        (r"/logout",LogoutHandler),
        (r"/(\w+)/Charles/1",BlogHandler),
        (r"/register",RegisterHandler),
        ]
        settings = {"cookie_secret" :"61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",\
                "static_path" : os.path.join(os.path.dirname(__file__), "static"),
                "debug":True
        }
        conn = pymongo.Connection("localhost",27017)
        self.db = conn.blog
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
    HTTPSERVER = tornado.httpserver.HTTPServer(Application())
    HTTPSERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

