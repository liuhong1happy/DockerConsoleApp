#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.application import ApplicationService
from services.application_access import ApplicationAccessService
import tornado.web
from tornado import gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings
from views import AsyncBaseHandler
import time

class ApplicationRunHandler(AsyncBaseHandler):
    s_application = ApplicationService()
    @gen.coroutine
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
        result = yield self.s_application.insert_application(insertData)
        # 加入队列
        msg = Message( json.dumps({
            "application_id":result["_id"],
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
            insertData["_id"] = result["_id"]
            self.write_result(data=insertData)

class ApplicationInfoHandler(AsyncBaseHandler):
    s_application = ApplicationService()
    @gen.coroutine
    def _post_(self):
        application_id = self.get_argument("application_id",None)
        app = yield self.s_application.find_one(application_id)
        app["_id"] = str(app["_id"])
        if app is None:
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
        "user_name":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True,
        "run_host":True,
        "inspect_container":True,
        "address_prefix":True,
        "singleton":True
    }
    @gen.coroutine
    def _get_(self):
        spec_type = self.get_argument("spec_type","app_name")
        spec_text =  self.get_argument("spec_text","")
        page_index =int(self.get_argument("page_index",0))
        page_size =int(self.get_argument("page_size",20))
        spec ={}
        spec[spec_type]={ '$regex' : spec_text}
        spec["user_id"] = str(self.current_user.get("_id",None))
        applications =yield self.s_application.get_appliactions(spec,fields=self.fields,page_index=page_index,page_size=page_size)
        if not applications:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=applications)
            
class ApplicationAccessHandler(AsyncBaseHandler):
    s_application = ApplicationService()
    s_application_access = ApplicationAccessService()
    
    @gen.coroutine
    def _get_(self):
        access_id = self.get_argument("id",None)
        access_info =  yield   s_application_access.find_one(access_id)
        if access_info is None:
            self.render_error(error_code=404,msg="not data")
        else:
            self.write_result(data=access_info)
    
    @gen.coroutine
    def _post_(self):
        access_type = self.get_argument("type",None)
        application_id = self.get_argument("id",None)
        access_content = self.get_argument("content","")

        container_info =yield self.s_application.find_one(application_id)
        if container_info is None:
            container_info = {}
        # 从数据库获取，切记不要对外公开
        container_host = container_info["run_host"]
        container_name = container_info["app_name"]
        user_id = str(self.current_user.get("_id",None))
        user_name = str(self.current_user.get("name",None))
        create_time = time.time()
        # 数据库操作
        accessData = {}
        accessData["access_type"] = access_type
        accessData["application_id"] = application_id
        accessData["container_name"] = container_name
        accessData["container_host"] = container_host
        accessData["access_content"] = access_content
        accessData["user_id"] = user_id
        accessData["status"] = 'start'
        accessData["logs"] = [
          {
            "create_time":create_time,
            "info":"started access application:"+application_id+",it is hosted in "+container_host,
            "user_id":user_id
          }
        ]
        result= yield self.s_application_access.access_application(accessData)
        print result
        # 加入队列
        msg = Message( json.dumps({
            "access_id":result,
            "access_type":access_type,
            "access_content":access_content,
            "application_id":application_id,
            "container_host":container_host,
            "container_name":container_name,
            "user_id":user_id,
            "user_name":user_name,
            "reply_to":'access_logs'
        }))
        send_message(msg,settings.ACCESS_APPLICATION_EXCHANGE,settings.ACCESS_APPLICATION_ROUTING+"."+container_host)
        if result is None:
            self.render_error(error_code=404,msg="not data")
        else:
            accessData["_id"] = str(result)
            self.write_result(data=accessData)
