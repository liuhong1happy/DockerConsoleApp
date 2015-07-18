#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.service import ServiceService
import tornado.web
import tornado.gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings

    
class GitLabOAuthHandler(tornado.web.RequestHandler):
    s_oauth = OAuthService()
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        spec_type = self.get_argument("spec_type","name")
        spec_text =  self.get_argument("spec_text","")
        page_index =int(self.get_argument("page_index",0))
        page_size =int(self.get_argument("page_size",20))
        spec ={}
        spec[spec_type]={ '$regex' : spec_text}
        fields={
            "name":True,
            "user":True,
            "image":True,
            "code":True,
            "status":True,
            "logs":True,
            "update_time":True,
            'create_time':True
        }

        services =yield tornado.gen.Task(self.s_service.get_list,spec,fields=fields,page_index=page_index,page_size=page_size)
        _json = ""
        if not services:
            _json =json.dumps({"status":"error","error_code":404})
        else:
            _json = json.dumps({"status":"success","data":services})
        self.write(_json)
        self.finish()
