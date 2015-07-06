#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado import gen
import tornado.httpserver
import os.path

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler)
        ]
        settings = dict(
            blog_title=u"Docker中文翻译社区",
            template_path=os.path.join(os.path.dirname(__file__), "dist"),
            static_path=os.path.join(os.path.dirname(__file__), "dist"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/login",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
