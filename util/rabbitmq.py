from tornado.options import define,options
from stormed import Connection,Message
import settings
import logging
from tornado.ioloop import IOLoop

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
    init_queue()

def init_queue():
    ch = conn.channel()
    ch.exchange_declare(exchange= settings.CREATE_SERVICE_EXCHANGE , type='direct',durable=True)
    ch.queue_declare(queue=settings.CREATE_SERVICE_QUEUE,durable=True)
    ch.queue_bind(queue=settings.CREATE_SERVICE_QUEUE,
                  exchange=settings.CREATE_SERVICE_EXCHANGE,
                  routing_key=settings.CREATE_SERVICE_ROUTING)
    logging.info("Declare amqp queue and exchange")

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
  
