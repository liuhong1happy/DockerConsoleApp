import tornado.web
from views import BaseHandler
class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")