from tornado.options import define, options
import asyncmongo

define("db_client", default=None, help="mongodb client", type=asyncmongo.client.Client)
define("etcd_client", default=None, help="etcd client", type=object)
define("docker_client", default=None, help="docker client", type=object)

SITE_URL = 'http://127.0.0.1:8888'
TORNADO_PORT = 8888

MONGO_POOL_ID = "DockerConsoleApp"
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'admin'
MONGO_USER = 'mongo'
MONGO_PWD = '123456'

ETCD_HOST = '127.0.0.1'
ETCD_PORT = 4001

DOCKER_HOST = 'unix:///var/run/docker.sock'