#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.service import ServiceService
import tornado.web
import tornado.gen
import tornado.escape
import json
class ServiceHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        service_id = self.get_argument("id")
        fields={
            "name":True,
            "user":True,
            "image":True,
            "ports":True,
            "envirements":True,
            "logo":True
        }
        service = tornado.gen.Task(s_service.get_one,service_id,fields=fields)
        
        if not service:
            json = tornado.escape.json_decode({"status":"error","error_code":404})
        else:
            json = tornado.escape.json_decode({"status":"success","data":service})
        self.write(json)
        self.finish()
    
    @tornado.web.asynchronous
    def post(self):
        git_path = self.get_argument("git_path",None)
        name = self.get_argument("service_name",None)
        user_name = self.get_argument("user_name","admin")
        # 数据库操作
        
        # 加入队列
        conn = options.mq_connection
        ch = conn.chanel()
        massage = Message({
            code:git_path,
            name:name,
            user:user_name,
            reply:'service_logs'
        })
        ch.exchange_declare(exchange='create_service', type='direct',durable=True)
        self.ch.queue_declare(queue='create_service',durable=True)
        self.ch.queue_bind(queue='create_service',exchange='create_service',routing_key='create_service')
        ch.publish(msg, exchange='create_service', routing_key='create_service')
    
class GetServiceLogsHandler(tornado.web.RequestHandler):
    def get(self):
        service_id = self.get_argument("id")
        fields={
            "logs":True,
            "status":True
        }
        service = tornado.gen.Task(s_service.get_one,service_id,fields=fields)
        
        if not service:
            json = tornado.escape.json_decode({"status":"error","error_code":404})
        else:
            json = tornado.escape.json_decode({"status":"success","data":service})
        self.write(json)
        self.finish()
    
class ServicesHandler(tornado.web.RequestHandler):
    s_service = ServiceService()
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        spec_type = self.get_argument("spec_type","name")
        spec_text =  self.get_argument("spec_text","")
        page_index =int(self.get_argument("page_index",0))
        page_size =int(self.get_argument("page_size",20))
        spec ={}
        spec[spec_type]=spec_text
        fields={
            "name":True,
            "user":True,
            "image":True,
            "code":True,
            "status":True,
            "logs":True,
            "update_time":True
        }

        services =yield tornado.gen.Task(self.s_service.get_list,spec,fields=fields,page_index=page_index,page_size=page_size)
        _json = ""
        if not services:
            _json =json.dumps({"status":"error","error_code":404})
        else:
            _json = json.dumps({"status":"success","data":services})
        self.write(_json)
        self.finish()
