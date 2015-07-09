from tornado.options import define,options
from stormed import Connection
import settings

def declare_mq():
  

def init_amqp():
  conn = Connection(host=settings.MQ_HOST,username=settings.MQ_USERNAME,
      password=settings.MQ_PASSWORD,heartbeat=settings.MQ_HEARTBEAT)
  

  
