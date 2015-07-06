import logging 
import asyncmongo
from tornado.options import define, options

define("mongo_client", default=None, help="mongodb client", type=asyncmongo.client.Client)

def init_db():
    db_client = None;
    try:
        db_client = asyncmongo.Client(
            pool_id='DockerConsoleApp', host='127.0.0.1', port=27017, 
            maxcached=10, maxconnections=50, dbname='admin')
        options.mongo_client = db_client
        logging.info("Init db successed")
    except Exception,e:
        logging.error("Init db failed",e);

    return db_client