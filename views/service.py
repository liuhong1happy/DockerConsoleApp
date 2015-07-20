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
from views import AsyncBaseHandler

class ServiceHandler(AsyncBaseHandler):
    s_service = ServiceService()
    fields={
        "name":True,
        "user":True,
        "image":True,
        "ports":True,
        "envirements":True,
        "logo":True
    }
    
    def _get_(self):
        service_id = self.get_argument("id")
        service = tornado.gen.Task(self.s_service.get_one,service_id,fields=self.fields)
        if not service:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=service)
    
    def _post_(self):
        git_path = self.get_argument("git_path",None)
        name = self.get_argument("service_name",None)
        user_name = self.current_user.get("name","admin")
                
        # 数据库操作
        insertData = {}
        insertData["code"] = git_path
        insertData["name"] = name
        insertData["user"] = user_name
        insertData["status"] = 'created'
        
        result= yield tornado.gen.Task(self.s_service.insert_service,insertData)
        
        # 加入队列
        msg = Message( json.dumps({
            "code":git_path,
            "name":name,
            "user":user_name,
            "reply_to":'service_logs'
        }) )
        
        send_message(msg,settings.CREATE_SERVICE_EXCHANGE,settings.CREATE_SERVICE_ROUTING)
        
        if not result:
            self.render_error(error_code=404,msg="not data")
        else:
            insertData["_id"] = str(result)
            self.write_result(data=insertData)
    
class GetServiceLogsHandler(AsyncBaseHandler):
    def _get_(self):
        service_id = self.get_argument("id")
        fields={
            "logs":True,
            "status":True
        }
        service = tornado.gen.Task(s_service.get_one,service_id,fields=fields)
        if not service:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=service)

class ServicesHandler(AsyncBaseHandler):
    s_service = ServiceService()
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
    def _get_(self):
        spec_type = self.get_argument("spec_type","name")
        spec_text =  self.get_argument("spec_text","")
        page_index =int(self.get_argument("page_index",0))
        page_size =int(self.get_argument("page_size",20))
        spec ={}
        spec[spec_type]={ '$regex' : spec_text}
        services =yield tornado.gen.Task(self.s_service.get_list,spec,fields=self.fields,page_index=page_index,page_size=page_size)
        _json = ""
        if not services:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=services)
