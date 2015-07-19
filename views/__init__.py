#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from pycket.session import SessionMixin
import json

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('user')
    
    def set_current_user(self,user):
        self.session.set('user', user)
        
    def write_result(self,data=[]):
        self.write(json.dumps({"status":"success","data":data}))
        self.finish()
    
    def render_error(self,error_code=404,msg="error msg"):
        self.write(json.dumps({"status":"error","error_code":error_code,'msg':msg}))
        self.finish()
        
class AsyncBaseHandler(BaseHandler):
    def _post_(self):
        pass

    def _get_(self):
        pass
    
    def _put_(self):
        pass
    
    def _delete_(self):
        pass
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        if self.current_user is None:
            self.render_error(error_code=1101,msg="API调用失败,请登录")
            self.finish()
        else:
            self._get_()
        
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        if self.current_user is None:
            self.render_error(error_code=1101,msg="API调用失败,请登录")
            self.finish()
        else:
            self._post_()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def put(self):
        if self.current_user is None:
            self.render_error(error_code=1101,msg="API调用失败,请登录")
            self.finish()
        else:          
            self._put_()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def delete(self):
        if self.current_user is None:
            self.render_error(error_code=1101,msg="API调用失败,请登录")
            self.finish()
        else:    
            self._delete_()        