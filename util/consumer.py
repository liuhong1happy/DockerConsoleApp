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
    logging.info("Declare amqp queue and exchange")
    
def init_consumer():
    ch = conn.channel()
    ch.consume(settings.CREATE_SERVICE_QUEUE,create_service,no_ack=False)
    logging.info("Init amqp consumer success")

def init_amqp():
    def handle_error(conn_error):
            print conn_error.method
            print conn_error.reply_code
    conn.on_error = handle_error
    
    def handle_disconnect():
            logging.error("Init amqp failed")
            options.ioloop.stop()
    conn.on_disconnect = handle_disconnect
    conn.connect(on_connect)

def send_message(message,exchange_name,routing_key):
    ch = conn.channel()
    ch.publish(msg, exchange=exchange_name, routing_key=routing_key)
    
def build_context(code):
    p = subprocess.Popen("curl -u 'liuhong1happy:wodexinmima96971' https://api.github.com/repos/Dockerlover/docker-ubuntu/contents", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line
    retval = p.wait()

    
def create_images(reply_to,code,name,user):
    cli = options.docker_client
    # 获取上下文 (tar文件)
    fp = open("docker-ubuntu.tar","r") 
    
    tag = settings.DOCKER_TAGPREFIX +"/"+user+"/"+name
    for line in cli.build(fileobj=fp, rm=True, tag=tag,custom_context=True):
        print line

    for line in cli.push( tag, stream=True,insecure_registry= settings.DOCKER_REGISTRY):
        print line
    
def create_service(msg):
    loadedData = json.loads(msg.body)
    reply_to = loadedData.get('reply_to')
    code = loadedData.get("code",None)
    name = loadedData.get("name",None)
    user = loadedData.get("user","admin")
    create_images(reply_to,code,name,user)
    msg.ack()