# -*-coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import time
import os

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
        self.write("logout!")

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
        self.write('<html><body><form action="/login" method="post">'
                'Name: <input type="text" name="name">'
                'Password: <input type="text" name="pass">'
                '<input type="submit" value="Sign in">'
                '</form></body></html>')
    def post(self):
        self.readuserinfo()
        usr = self.get_argument("name",'')
        password = self.get_argument("pass",'')
        if not self.data.has_key(usr) or self.data[usr] != password:
            self.render('http://thebest404pageever.com/')
        if usr != '' and password != '':
            self.set_secure_cookie("user",usr)
            make_url = "/" + usr + "/Charles/1"
            self.redirect(make_url)
        else:
            self.redirect("/login")

class BlogHandler(BaseHandler):
    """
    Implements basic handler
    """
    flag = False
    user = []
    def readuserinfo(self):
        fr = open('./data/users.txt','r')
        infomation = fr.readlines()
        for line in infomation:
            match = line[:-1].split(',')
            self.user.append(match[0])
        fr.close()
    def get(self,author_name):
        self.readuserinfo()
        if not author_name in self.user:
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
        fr = open('./data/comments.txt','r')
        infomation = fr.readlines()
        for line in infomation:
            sth = line[:-1].split('|')
            item = []
            item.append(sth[0])
            item.append(sth[1])
            item.append(sth[2])
            comment.append(item)

        fr.close()
        if author_name != self.current_user:
            self.flag = False
        self.render('./template.html', passtitle = tem[0], \
         author = tem[1], blog = tem[2] , comment = comment,flag = self.flag)
    def post(self, info):
        fw = open('./data/comments.txt','a')
        new_comment = self.get_argument("comment_submit")
        usr = self.current_user
        newtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        fw.write(usr+"|" + newtime + "|" + new_comment.encode('utf-8') + "\n")
        fw.close()
        new_url="/" + usr + "/Charles/1"
        self.redirect(new_url)


application = tornado.web.Application([
        (r"/",MainHandler),
        (r"/login",LoginHandler),
        (r"/logout",LogoutHandler),
        (r"/(\w+)/Charles/1",BlogHandler),
        ],cookie_secret ="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",\
        static_path =os.path.join(os.path.dirname(__file__), "static"),
        debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

