#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.options import define,options
from stormed import Connection,Message
import settings
import logging
from tornado.ioloop import IOLoop
import json
import pycurl
import StringIO
import subprocess
from util.oauth import GitLabOAuth2Mixin
from services.oauth import OAuthService
from services.service import ServiceService
from services.application import ApplicationService
from tornado.httputil import HTTPHeaders
from tornado import gen
from bson.objectid import ObjectId
import md5
import time
import random

conn = Connection(host=settings.MQ_HOST,username=settings.MQ_USERNAME,
      password=settings.MQ_PASSWORD,heartbeat=settings.MQ_HEARTBEAT)
msg = Message('Hello World!')

def callback(msg):
    logging.info(" test=> Received %r" % msg.body)

def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='hello')
    ch.publish(msg, exchange='', routing_key='hello')
    logging.info(" test=> Sent 'Hello World!'")
    ch.consume('hello', callback, no_ack=True)
    
    logging.info("Init amqp success")
    options.mq_connection = conn
    # 初始化队列
    init_queue()
    # 初始化消费者
    init_consumer()

def init_queue():
    ch = conn.channel()
    
    ch.exchange_declare(exchange= settings.CREATE_SERVICE_EXCHANGE , type='direct',durable=True)
    ch.queue_declare(queue=settings.CREATE_SERVICE_QUEUE,durable=True)
    ch.queue_bind(queue=settings.CREATE_SERVICE_QUEUE,
                  exchange=settings.CREATE_SERVICE_EXCHANGE,
                  routing_key=settings.CREATE_SERVICE_ROUTING)

    ch.exchange_declare(exchange= settings.RUN_APPLICATION_EXCHANGE , type='direct',durable=True)
    ch.queue_declare(queue=settings.RUN_APPLICATION_QUEUE,durable=True)
    ch.queue_bind(queue=settings.RUN_APPLICATION_QUEUE,
                  exchange=settings.RUN_APPLICATION_EXCHANGE,
                  routing_key=settings.RUN_APPLICATION_ROUTING)

    logging.info("Declare amqp queue and exchange")
    
def init_consumer():
    ch = conn.channel()
    ch.consume(settings.CREATE_SERVICE_QUEUE,create_service,no_ack=False)
    ch.consume(settings.RUN_APPLICATION_QUEUE,run_application,no_ack=False)
    logging.info("Init amqp consumer success")

def init_amqp():
    def handle_error(conn_error):
            logging.error("Init amqp error")
    conn.on_error = handle_error
    
    def handle_disconnect():
            logging.error("Init amqp failed")
            options.ioloop.stop()
    conn.on_disconnect = handle_disconnect
    conn.connect(on_connect)

def send_message(message,exchange_name,routing_key):
    ch = conn.channel()
    ch.publish(msg, exchange=exchange_name, routing_key=routing_key)

def create_service(msg):
    build_context = json.loads(msg.body)
    builder = BuildImage(build_context)
    builder.start_build_context()
    msg.ack()

def run_application(msg):
    start_context = json.loads(msg.body)
    builder = StartContainer(start_context)
    builder.start_run_application()
    msg.ack()

class BuildImage():
    s_service = ServiceService()
    def __init__(self,build_context):
        self._build_context = build_context
        
    @gen.coroutine
    def get_access_token(self,user_id):
        s_oauth = OAuthService()
        token = yield s_oauth.get_gitlab_token(ObjectId(user_id))
        raise gen.Return(token)
    
    # 随机生产md5加密的hash码
    def gen_md5(self):
        m = md5.new()  
        project_name = self._build_context.get("project_name",None)
        random_float = random.uniform(0, 1000)
        current_time = time.time()
        m.update(str(project_name)+str(random_float)+str(current_time))
        return m.hexdigest()  
    
    # 获取代码并构建上下文
    @gen.coroutine
    def start_build_context(self):
        # 随机生产文件名称，并删除可能存在的文件
        project_name = self._build_context.get("project_name",None)
        self._md5 = self.gen_md5()
        self._file_name = "/tmp/build_image/"+project_name+"-"+self._md5+".tar"
        self.delete_tar_file(self._file_name)
        # 获取当前项目下的构建日志
        project_url = self._build_context.get("project_url",None)
        service = yield self.s_service.find_one({"project_url":project_url},fields=None)
        logs = service["logs"]
        if logs is None:
            logs = []
        if not isinstance(logs,list):
            logs = []
        self._build_context["logs"] = logs
        self.update_database("running")
        # 获取当前用户下的access_token
        user_id = self._build_context.get("user_id",None)
        token = yield self.get_access_token(user_id)
        self._access_token = token["access_token"]["access_token"]
        # 根据project_id组建获取master分支附件的url
        project_id = self._build_context.get("project_id",None)
        self._archive_url = '/api/v3/projects/'+project_id+'/repository/archive'
        # 记录操作日志
        self._build_context["logs"].append({"info":u"保存项目master分支附件到指定路径："+self._file_name,"user_id":user_id,"create_time":time.time()})
        self._build_context["logs"].append({"info":u"获取当前用户下的access_token："+self._access_token,"user_id":user_id,"create_time":time.time()})
        self._build_context["logs"].append({"info":u"根据project_id组建获取master分支附件的url："+self._archive_url ,"user_id":user_id,"create_time":time.time()})
        self._build_context["logs"].append({"info":u"开始从"+self._archive_url+"获取master分支附件" ,"user_id":user_id,"create_time":time.time()})
        self.update_database("running")
        # 开始获取代码并开始构建
        oauth_access = GitLabOAuth2Mixin()
        headers = HTTPHeaders({"Content-Type": "application/octet-stream","Content-Transfer-Encoding":"binary"})
        oauth_access.get_by_api(self._archive_url ,access_token=self._access_token,
                                streaming_callback=self.save_tar_file
                                ,headers=headers,
                                callback=self.build_image)
        
        
    # 预判文件是否存在，如果存在则删除 
    def delete_tar_file(self,file_name):
        import os
        if os.path.exists(file_name):
            os.remove(file_name)
            
    # 保存代码到文件系统
    def save_tar_file(self,blob):
        self._build_context["logs"].append({"info":u"从"+self._archive_url+"获取大小"+len(blob)+"的附件数据" ,"user_id":user_id,"create_time":time.time()})
        WriteFileData = open(self._file_name,'ab')
        WriteFileData.write(blob)
        WriteFileData.close()
        self.update_database("running")
    
    # 根据上下文构建
    def build_image(self):
        self._build_context["logs"].append({"info":u"获取附件完成，开始构建镜像" ,"user_id":user_id,"create_time":time.time()})
        cli = options.docker_client
        fp = open(self._file_name,"r")
        tag = settings.DOCKER_TAGPREFIX +"/"+user+"/"+name
        for line in cli.build(fileobj=fp, rm=True, tag=tag,custom_context=True):
            # 写入数据库
            self._build_context["logs"].append({"info":line ,"user_id":user_id,"create_time":time.time()})
            self.update_database("running")
        fp.close()
        self.delete_tar_file(self._file_name)
        self._build_context["logs"].append({"info":u"构建镜像完成，开始push镜像" ,"user_id":user_id,"create_time":time.time()})
        for line in cli.push( tag, stream=True,insecure_registry= settings.DOCKER_REGISTRY):
            # 写入数据库
            self._build_context["logs"].append({"info":line ,"user_id":user_id,"create_time":time.time()})
            self.update_database("running")
        self.update_database("success")
        
    # 更新数据库
    @gen.coroutine
    def update_database(self,status):
        self._build_context["status"] = status
        result = yield self.s_service.insert_service(self._build_context)

class StartContainer():
    s_application = ApplicationService()
    def __init__(self,start_context):
        self._start_context = start_context
