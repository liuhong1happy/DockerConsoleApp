#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.options import define, options
import pymongo
# 基本链接信息
define("db_client", default=None, help="mongodb client", type=pymongo.mongo_client.MongoClient)
define("etcd_client", default=None, help="etcd client", type=object)
define("docker_client", default=None, help="docker client", type=object)
define("mq_connection", default=None, help="amqp connection", type=object)
# 常用枚举变量
define("service_status", default={
        "created":0,
        "running":1,
        "success":2
    }, help="service status", type=dict)

SITE_URL = 'http://192.168.0.110:8888'
TORNADO_PORT = 8888

MONGO_POOL_ID = "DockerConsoleApp"
MONGO_HOST = '192.168.0.110'
MONGO_PORT = 27017
MONGO_DB = 'admin'
MONGO_USER = 'mongo'
MONGO_PWD = '123456'

ETCD_HOST = '192.168.0.110'
ETCD_PORT = 4001

DOCKER_HOST = 'unix:///var/run/docker.sock'
# docker registry 
DOCKER_REGISTRY = "http://192.168.0.110:5000"
# docker pull tag prefix (don't have string 'http://')
DOCKER_TAGPREFIX = "192.168.0.110:5000"

MQ_HOST = '192.168.0.110'
MQ_HEARTBEAT = 30
MQ_USERNAME = 'admin'
MQ_PASSWORD = 'testpass'

# queue declare
CREATE_SERVICE_EXCHANGE = 'create_service_exchange'
CREATE_SERVICE_QUEUE = 'create_service_queue'
CREATE_SERVICE_ROUTING = 'create_service_routing'

# gitlab settings
GITLAB_SITE_URL = 'http://192.168.0.110:10080'
GITLAB_OAUTH = {
    "authorize_url":GITLAB_SITE_URL+"/oauth/authorize",
    "access_token_url":GITLAB_SITE_URL+"/oauth/token",
    "user_info_url":GITLAB_SITE_URL+"/api/v3/user",
    "redirect_url":SITE_URL+'/api/gitlab/oauth',
    "key":'9c7a33a2ed9dbe2ef77d91f9fd9c27de495ad8a68ae0609556401b09f7245d98',
    "secret":'2b389ac2adb9a296981bc150aac272bc053f9f2ff3f8a8e79dba444240e4aabf'
}

# redis 
REDIS_HOST = '192.168.0.110'
REDIS_PORT = '6379'
REDIS_PASS = ''
