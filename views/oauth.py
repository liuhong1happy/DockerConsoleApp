#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.oauth import OAuthService
import tornado.web
import tornado.gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings
from views import AsyncBaseHandler
import libcurl
import pycurl
import tornado.curl_httpclient

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

class GitLabAuthHandler(AsyncBaseHandler):
    @tornado.gen.engine
    def _get_(self):
        return_code = self.get_argument('code')
        user_id = self.current_user.get('_id',None)
        if user_id is None:
            render_error(error_code=404,msg='not user data')
            return
        user = yield tornado.gen.Task(self.s_oauth.udpate_gitlab_token,user_id,{
          "code":code
        })
        # 使用http client请求token
        respose = yield tornado.gen.Task(self.request_token,code)
        if respose is None:
            write_result(data=respose)
        else:
            render_error(error_code=404,msg='not user data')
    
    @tornado.gen.engine
    def request_token(self,code,callback=None):
        http_client = AsyncHTTPClient()
        response = yield gen.Task(http_client.fetch, "http://example.com",method=POST, body=json.dumps(data))
        callback(response)

class GitLabTokenHandler(AsyncBaseHandler):
    s_oauth = OAuthService()
    @tornado.gen.engine
    def _get_(self):
        user_id = self.current_user.get('_id',None)
        if user_id is None:
            render_error(error_code=404,msg='not user data')
            return
        
        token = yield tornado.gen.Task(self.s_oauth.get_gitlab_token,user_id)
        
        if token is None:
            self.write_result(data=token)
        else:
            self.render_error(error_code=404,msg='not user data')

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
            

