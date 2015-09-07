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
from services.application_access import ApplicationAccessService
from tornado.httputil import HTTPHeaders
from tornado import gen
from bson.objectid import ObjectId
import md5
import time
import random
import os
import tarfile
from tornado.httpclient import AsyncHTTPClient
from docker.utils import create_host_config
from docker.errors import APIError
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

    ch.exchange_declare(exchange= settings.ACCESS_APPLICATION_EXCHANGE , type='topic',durable=True)
    ch.queue_declare(queue=settings.ACCESS_APPLICATION_QUEUE,durable=True)
    ch.queue_bind(queue=settings.ACCESS_APPLICATION_QUEUE,
                  exchange=settings.ACCESS_APPLICATION_EXCHANGE,
                  routing_key=settings.ACCESS_APPLICATION_ROUTING+"."+settings.CURRENT_HOST)

    logging.info("Declare amqp queue and exchange")
    
def init_consumer():
    ch = conn.channel()
    ch.consume(settings.CREATE_SERVICE_QUEUE,create_service,no_ack=False)
    ch.consume(settings.RUN_APPLICATION_QUEUE,run_application,no_ack=False)
    ch.consume(settings.ACCESS_APPLICATION_QUEUE,access_application,no_ack=False)
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

def access_application(msg):
    access_context = json.loads(msg.body)
    builder = AccessContainer(access_context)
    builder.start_access_application()
    msg.ack()

class BuildImage():
    s_service = ServiceService()
    def __init__(self,build_context):
        self._build_context = build_context
        AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        
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
    
    def get_tar_file(self,arcpath,tar_file,content_path):
        new_tar_file = tar_file+".gz";
        t = tarfile.open(tar_file)
        t.extractall(path = arcpath) 
        t.close()
        self.delete_tar_file(tar_file)
        tz = tarfile.open(new_tar_file, "w:gz")
        for root, dir, files in os.walk(arcpath):
            for file in files:
                fullpath = os.path.join(root, file)
                tz.add(fullpath,arcname=file)
        tz.close()
        return new_tar_file
    
    # 获取代码并构建上下文
    @gen.coroutine
    def start_build_context(self):
        # 随机生产文件名称，并删除可能存在的文件
        project_name = self._build_context.get("project_name",None)
        self._md5 = self.gen_md5()
        if(not os.path.exists("/tmp/build_image")):
            os.mkdir("/tmp/build_image")
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
        self._user_id = self._build_context.get("user_id",None)
        self._user_name = self._build_context.get("user_name",None)
        token = yield self.get_access_token(self._user_id)
        self._access_token = token["access_token"]["access_token"]
        # 根据project_id组建获取master分支附件的url
        project_id = self._build_context.get("project_id",None)
        self._archive_url = '/api/v3/projects/'+project_id+'/repository/archive'
        # 记录操作日志
        self._build_context["logs"].append({"info":u"保存项目master分支附件到指定路径："+self._file_name,"user_id":self._user_id,"create_time":time.time()})
        self._build_context["logs"].append({"info":u"获取当前用户下的access_token："+self._access_token,"user_id":self._user_id,"create_time":time.time()})
        self._build_context["logs"].append({"info":u"根据project_id组建获取master分支附件的url："+self._archive_url ,"user_id":self._user_id,"create_time":time.time()})
        self._build_context["logs"].append({"info":u"开始从"+self._archive_url+u"获取master分支附件" ,"user_id":self._user_id,"create_time":time.time()})
        self.update_database("running")
        # 开始获取代码并开始构建
        http = AsyncHTTPClient()
        headers = HTTPHeaders({"Content-Type": "application/octet-stream","Content-Transfer-Encoding":"binary"})
        http.fetch(settings.GITLAB_SITE_URL+self._archive_url +"?access_token="+self._access_token,self.build_image,
                   streaming_callback=self.save_tar_file,
                   headers=headers)
        
    # 预判文件是否存在，如果存在则删除 
    def delete_tar_file(self,file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
            
    # 保存代码到文件系统
    def save_tar_file(self,blob):
        self._build_context["logs"].append({"info": u"从"+self._archive_url+u"获取大小"+str(len(blob))+u"的附件数据" ,"user_id":self._user_id,"create_time":time.time()})
        WriteFileData = open(self._file_name,'ab')
        WriteFileData.write(blob)
        WriteFileData.close()
        self.update_database("running")
    
    # 根据上下文构建
    def build_image(self,response):
        if response.error:
            return
        project_name = self._build_context.get("project_name",None)
        self._file_name = self.get_tar_file("/tmp/build_image/"+project_name+"-"+self._md5,"/tmp/build_image/"+project_name+"-"+self._md5+".tar",project_name+".git")
        self._build_context["logs"].append({"info":u"获取附件完成，开始构建镜像" ,"user_id":self._user_id,"create_time":time.time()})
        cli = options.docker_client
        fp = open(self._file_name,"r")
        tag = settings.DOCKER_TAGPREFIX +"/"+self._user_name+"/"+project_name
        self._build_context["storage_path"] = tag
        import json
        for line in cli.build(fileobj=fp, rm=True, tag=tag,custom_context=True,forcerm=True,pull=False):
            newLine = json.loads(line)
            newLog = {"info":newLine ,"user_id":self._user_id,"create_time":time.time()}
            if(isinstance(self._build_context["logs"][-1]["info"],dict)):
                status = self._build_context["logs"][-1]["info"].get("status",None)
                print status,newLine.get("status",None),status == newLine.get("status",None)
                if status is None:
                    self._build_context["logs"].append(newLog)
                elif status == newLine.get("status",None):
                    self._build_context["logs"][-1] = newLog
                else:
                    self._build_context["logs"].append(newLog)
            else:
                self._build_context["logs"].append(newLog)
            # 写入数据库
            self.update_database("running")
        fp.close()
        self.delete_tar_file(self._file_name)
        self._build_context["logs"].append({"info":u"构建镜像完成，开始push镜像" ,"user_id":self._user_id,"create_time":time.time()})
        for line in cli.push( tag, stream=True,insecure_registry=True):
            # 写入数据库
            self._build_context["logs"].append({"info":line ,"user_id":self._user_id,"create_time":time.time()})
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
        self._application_id = self._start_context["application_id"]
        self._storage_path = self._start_context["storage_path"]
        self._user_id = self._start_context["user_id"]
        self._project_url = self._start_context["project_url"]
        self._project_name = self._start_context["project_name"]
        self._user_name =  self._start_context["user_name"]
        self._app_prefix = self._user_name+"-"+self._project_name+"-"
       
    
    def start_run_application(self):
        self.pull_image()
        self.start_container()
    
    @gen.coroutine
    def pull_image(self):
        application = yield self.s_application.find_one(self._application_id)
        if application is None:
            return
        logs = application["logs"]
        if logs is None:
            logs = []
        if not isinstance(logs,list):
            logs = []
        self._start_context["logs"] = []
        cli = options.docker_client
        self._start_context["logs"].append({"info":"starting pull image:"+self._storage_path ,"user_id":self._user_id,"create_time":time.time()})
        for line in cli.pull(self._storage_path,stream=True,insecure_registry=True):
            self._start_context["logs"].append({"info":line ,"user_id":self._user_id,"create_time":time.time()})
        
    def start_container(self):
        host_config = create_host_config(publish_all_ports=True,restart_policy={'Name':'always'})
        app_name = self._app_prefix+str(1)
        cli = options.docker_client
        try:
            cli.remove_container(container=app_name,force=True)
        except APIError,e:
            logging.info("can't find container")
        container = cli.create_container(image=self._storage_path,host_config=host_config,name=app_name)
        response = cli.start(container=app_name)
        self._start_context["container_id"] = container["Id"]
        self._start_context["app_name"] = app_name
        self._start_context["run_host"] = settings.CURRENT_HOST 
        self.update_database("success")
        
    @gen.coroutine
    def update_database(self,status):
        self._start_context["status"] = status
        result = yield self.s_application.insert_application(self._start_context)

class AccessContainer():
    s_application_access = ApplicationAccessService()
    s_application = ApplicationService()
    
    def __init__(self,access_context):
        self._access_context = access_context
        self._access_id = access_context["access_id"]
        self._user_id = self._access_context["user_id"]
        self._container_name = self._access_context["container_name"]
        self._application_id = self._access_context["application_id"]
        self._user_name =  self._access_context["user_name"]
        self._access_type =  self._access_context["access_type"]
        self._access_content =  self._access_context["access_content"]

    def start_access_application(self):
        if(self._access_type=="restart"):
            self.restart_container()
        if(self._access_type=="stop"):
            self.stop_container()
        if(self._access_type=="delete"):
            self.delete_container()
        if(self._access_type=="exec"):
            self.exec_container()
        if(self._access_type=="update"):
            self.update_container()
    
    def restart_container(self):
        cli = options.docker_client
        response = cli.start(container=self._container_name)
        self.update_application("restart")
        self._access_context["response"] = response
        self.update_database("success")
   
    def stop_container(self):
        cli = options.docker_client
        response = cli.stop(container=self._container_name)
        self.update_application("stop")
        self._access_context["response"] = response
        self.update_database("success")
    
    def delete_container(self):
        cli = options.docker_client
        response = None
        try:
            response = cli.remove_container(container=self._container_name,force=True)
        except Exception as e:
            pass
        self._access_context["response"] = response
        self.update_database("success")
    
    def exec_container(self):
        cli = options.docker_client
        exec_obj = cli.exec_create(container=self._container_name,cmd=self._access_content.slipt(' '))
        response = cli.exec_start(exec_id=exec_obj["Id"])
        self.update_application("exec:"+self._access_content)
        self._access_context["response"] = response
        self.update_database("success")
        
    def update_container(self):
        cli = options.docker_client
        self.update_application("update")
        self._access_context["response"] = "update"
        self.update_database("success")
    
    @gen.coroutine
    def update_application(self,access):
        cli = options.docker_client
        response = cli.inspect_container(container=self._container_name)
        application = {
            "application_id":self._application_id,
            "inspect_container":response,
            "singleton":settings.SINGLETON,
            "address_prefix": settings.DISCOVER_HOST if settings.SINGLETON else settins.DISCOVER_DOMAIN,
            "last_access":access,
            "last_access_id":self._access_id
        }
        application["update_result"] = yield self.s_application.insert_application(application)
        

    
    @gen.coroutine
    def update_database(self,status):
        self._access_context["status"] = status
        
        result = {}
        if(self._access_type == "delete"):
            application = yield self.s_application.find_one(ObjectId(self._application_id))
            application["application_id"] = self._application_id
            
            logging.info(self._application_id)
            logging.info(application["_id"])
            application["del_flag"] = True
            delObj = yield self.s_application.insert_application(application)
        result = yield self.s_application_access.access_application(self._access_context)
