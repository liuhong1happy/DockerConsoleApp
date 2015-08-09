#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.application import ApplicationService
import tornado.web
import tornado.gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings
from views import AsyncBaseHandler
import time

class ApplicationRunHandler(AsyncBaseHandler):
    s_application = ApplicationService()
    @tornado.gen.coroutine
    def _post_(self):
        project_url = self.get_argument("project_url",None)
        project_name = self.get_argument("project_name",None)
        storage_path = self.get_argument("storage_path",None)
        user_id = str(self.current_user.get("_id",None))
        user_name = str(self.current_user.get("name",None))
        create_time = time.time()

        # 数据库操作
        insertData = {}
        insertData["project_url"] = project_url
        insertData["project_name"] = project_name
        insertData["storage_path"] = storage_path
        insertData["user_id"] = user_id
        insertData["status"] = 'created'
        insertData["logs"] = [{"create_time":create_time,"info":"started run application:"+project_name,"user_id":user_id}]
        result= yield self.s_application.insert_application(insertData)
        # 加入队列
        msg = Message( json.dumps({
            "project_url":project_url,
            "project_name":project_name,
            "storage_path":storage_path,
            "user_id":user_id,
            "user_name":user_name,
            'app_count':1,
            "reply_to":'service_logs'
        }))
        send_message(msg,settings.RUN_APPLICATION_EXCHANGE,settings.RUN_APPLICATION_ROUTING)
        if result is None:
            self.render_error(error_code=404,msg="not data")
        else:
            insertData["_id"] = str(result)
            self.write_result(data=insertData)

class ApplicationInfoHandler(AsyncBaseHandler):
    s_application = ApplicationService()
    fields={
        "project_url":True,
        "project_name":True,
        "app_name":True,
        "user_id":True,
        "status":True,
        "logs":True
    }
    @tornado.gen.coroutine
    def _post_(self):
        app_name = self.get_argument("app_name",None)
        
        app = yield self.s_application.find_one({"app_name":app_name},fields=self.fields)
        app["_id"] = str(app["_id"])
        if service is None:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=app)

class ApplicationsHandler(AsyncBaseHandler):
    s_application = ApplicationService()
    fields={
        "project_url":True,
        "project_name":True,
        "app_name":True,
        "user_id":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }
    @tornado.gen.coroutine
    def _get_(self):
        spec_type = self.get_argument("spec_type","app_name")
        spec_text =  self.get_argument("spec_text","")
        page_index =int(self.get_argument("page_index",0))
        page_size =int(self.get_argument("page_size",20))
        spec ={}
        spec[spec_type]={ '$regex' : spec_text}
        applications =yield self.s_application.get_list(spec,fields=self.fields,page_index=page_index,page_size=page_size)
        if not services:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=applications)