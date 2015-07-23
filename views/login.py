#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.user import UserService
import tornado.web
import tornado.gen
import tornado.escape
import json
import settings
from util.stmp import send_email
from views import BaseHandler

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
    
class SigninHandler(BaseHandler):
    s_user = UserService()
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        name_or_email = self.get_argument("name_or_email")
        password =  self.get_argument("password")
        fields={
            "name":True,
            "email":True,
            "gitlab":True,
            "last_time":True,
            "login_time":True,
            "create_time":True,
            "password":True
        }
        user =yield self.s_user.signin(name_or_email, password,fields=fields)
        if user is None:
            self.render_error(error_code=404,msg="login failed")
        else:
            self.set_current_user(user)
            self.write_result()
    
class SignupHandler(BaseHandler):
    s_user = UserService()
    
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        name = self.get_argument("name")
        email =  self.get_argument("email")
        password =  self.get_argument("password")

        fields={
            "name":True,
            "email":True,
            "gitlab":True,
            "last_time":True,
            "login_time":True,
            "create_time":True,
            "password":True
        }

        hasName =yield self.s_user.find_one({"name":name}, fields = fields)
        hasEmail =yield  self.s_user.find_one({"email":email}, fields = fields)

        if( (hasName is not None) or (hasEmail is not None) ):
            self.render_error(error_code=404,msg='user exist')
        else:
            user = yield self.s_user.signup(name,email, password,fields)
            if not user:
                self.render_error(error_code=404,msg='signup failed')
            else:
                self.write_result(data=user)
        
class ForgetHandler(BaseHandler):
    s_user = UserService()
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        name = self.get_argument("email")
        # 重置密码
        user =yield self.s_user.forget(email)
        # 发送邮件
        send_email()

        if not user:
            self.write_result(msg='user not exist')
        else:
            self.write_result(data=user)