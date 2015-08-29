#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado import gen
import tornado.httpserver
import os.path
import settings
from util.db import init_db
from util.discover import init_etcd
from util.dockerclient import init_docker
from util.rabbitmq import init_amqp

define("port", default=settings.TORNADO_PORT, help="run on the given port", type=int)
define("ioloop",default=None,help="global ioloop instance",type=object)

class Application(tornado.web.Application):
    def __init__(self):
        self.init_service()
        from views.home import HomeHandler
        from views.service import ServicesHandler,ServiceInfoHandler,ServiceBuildHandler
        from views.login import LoginHandler,SigninHandler,SignupHandler,ForgetHandler
        from views.oauth import GitLabOAuthHandler,GitLabTokenHandler,GitLabRefreshHanlder
        from views.application import ApplicationsHandler,ApplicationInfoHandler,ApplicationRunHandler,ApplicationAccessHandler
        handlers = [
             (r"/", HomeHandler),
             (r"/login",LoginHandler),
             (r"/api/user/signup",SignupHandler),
             (r"/api/user/signin",SigninHandler),
             (r"/api/user/forget",ForgetHandler),
             (r"/api/services",ServicesHandler),
             (r"/api/service/info",ServiceInfoHandler),
             (r"/api/service/build",ServiceBuildHandler),
             (r"/api/applications",ApplicationsHandler),
             (r"/api/application/info",ApplicationInfoHandler),
             (r"/api/application/run",ApplicationRunHandler),
             (r"/api/application/access",ApplicationAccessHandler),
             (r"/api/gitlab/oauth",GitLabOAuthHandler),
             (r"/api/gitlab/token",GitLabTokenHandler),
             (r"/api/gitlab/refresh",GitLabRefreshHanlder)
        ]
        _settings = dict(
            blog_title=u"Docker中文翻译社区",
            template_path=os.path.join(os.path.dirname(__file__), "dist"),
            static_path=os.path.join(os.path.dirname(__file__), "dist"),
            xsrf_cookies=False,
            cookie_secret="AAAAB3NzaC1yc2EAAAADAQABAAABAQCww",
            login_url="/login",
            debug=True,
            pycket = {
                'engine': 'redis',
                'storage': {
                    'host': settings.REDIS_HOST,
                    'port':  settings.REDIS_PORT,
                    'db_sessions': 10,
                    'db_notifications': 11,
                    'max_connections': 2 ** 31,
                },
                'cookies': {
                    'expires_days': 120,
                },
            },
        )
        tornado.web.Application.__init__(self, handlers, **_settings)
    
    def init_service(self):
        init_db()
        init_etcd()
        init_docker()
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
