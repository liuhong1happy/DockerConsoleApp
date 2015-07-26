#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado import gen
import tornado.httpserver
import os.path
import settings



define("port", default=settings.TORNADO_PORT+1, help="run on the given port", type=int)
define("ioloop",default=None,help="global ioloop instance",type=object)

def create_service(msg):
    print " [x] %r:%r" % (msg.rx_data,msg.routing_key,msg.body)


class Application(tornado.web.Application):
    def __init__(self):
        self.init_service()

        handlers = []
        settings = dict(
            blog_title=u"Docker中文翻译社区",
            template_path=os.path.join(os.path.dirname(__file__), "dist"),
            static_path=os.path.join(os.path.dirname(__file__), "dist"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/login",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
    
    def init_service(self):
        from util.db import init_db
        init_db()
        from util.discover import init_etcd
        init_etcd()
        from util.dockerclient import init_docker
        init_docker()
        from util.consumer import init_amqp
        init_amqp()

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    
    ioloop_instance = tornado.ioloop.IOLoop.instance()
    options.ioloop = ioloop_instance
    ioloop_instance.start()

if __name__ == "__main__":
    main()


