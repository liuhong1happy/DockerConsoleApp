#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.user import UserService
import tornado.web
import tornado.gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings
from views import AsyncBashHandler

class GitLabOAuthHandler(AsyncBashHandler):
    s_oauth = OAuthService()
    
    @tornado.gen.engine
    def _post_(self):
        access_token = self.get_argument('access_token')
        gitlab_user = self.get_argument('user')
        current_user = self.current_user.get('_id','admin')
        
        user = yield tornado.gen.Task(self.s_oauth.update,current_user,{} )
