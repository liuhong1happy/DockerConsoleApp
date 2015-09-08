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
import time

class ServiceBuildHandler(AsyncBaseHandler):
    s_service = ServiceService()
    @tornado.gen.coroutine
    def _post_(self):
        project_url = self.get_argument("project_url",None)
        project_name = self.get_argument("project_name",None)
        project_id = self.get_argument("project_id",None)
        user_id = str(self.current_user.get("_id",None))
        user_name = str(self.current_user.get("name",None))
        create_time = time.time()

        # 数据库操作
        insertData = {}
        insertData["project_url"] = project_url
        insertData["project_name"] = project_name
        insertData["project_id"] = project_id
        insertData["user_id"] = user_id
        insertData["status"] = 'created'
        insertData["logs"] = [{"create_time":create_time,"info":'{"stream":"started build project:'+project_name+'"}',"user_id":user_id}]
        result= yield self.s_service.insert_service(insertData)
        # 加入队列
        msg = Message( json.dumps({
            "project_url":project_url,
            "project_name":project_name,
            "project_id":project_id,
            "user_id":user_id,
            "user_name":user_name,
            "reply_to":'service_logs'
        }))
        send_message(msg,settings.CREATE_SERVICE_EXCHANGE,settings.CREATE_SERVICE_ROUTING)
        if result is None:
            self.render_error(error_code=404,msg="not data")
        else:
            insertData["_id"] = str(result)
            self.write_result(data=insertData)

class ServiceInfoHandler(AsyncBaseHandler):
    s_service = ServiceService()
    fields={
        "project_url":True,
        "project_name":True,
        "project_id":True,
        "user_id":True,
        "status":True,
        "logs":True
    }
    @tornado.gen.coroutine
    def _post_(self):
        project_url = self.get_argument("project_url",None)
        project_name = self.get_argument("project_name",None)
        project_id = self.get_argument("project_id",None)
        
        service = yield self.s_service.find_one({"project_url":project_url},fields=self.fields)
        service["_id"] = str(service["_id"])
        if service is None:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=service)

class ServicesHandler(AsyncBaseHandler):
    s_service = ServiceService()
    fields={
        "project_url":True,
        "project_name":True,
        "project_id":True,
        "storage_path":True,
        "user_id":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }
    @tornado.gen.coroutine
    def _get_(self):
        spec_type = self.get_argument("spec_type","project_name")
        spec_text =  self.get_argument("spec_text","")
        page_index =int(self.get_argument("page_index",0))
        page_size =int(self.get_argument("page_size",20))
        spec ={}
        spec[spec_type]={ '$regex' : spec_text}
        services =yield self.s_service.get_list(spec,fields=self.fields,page_index=page_index,page_size=page_size)
        if not services:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=services)
