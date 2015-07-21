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
        token_type = self.get_argument('token_type')
        expires_in = self.get_argument('expires_in')
        refresh_token = self.get_argument('expires_in')
        user_id = self.current_user.get('_id',None)
        if user_id is None:
            render_error(error_code=404,msg='not user data')
            return
        
        user = yield tornado.gen.Task(self.s_oauth.udpate_gitlab_token,user_id,{
          "access_token":access_token,
          "token_type":token_type,
          "expires_in":expires_in,
          "refresh_token":refresh_token
        })
        
        if user is None:
            write_result(data=user)
        else:
            render_error(error_code=404,msg='not user data')
