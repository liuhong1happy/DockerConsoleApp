import logging 
import asyncmongo
from tornado.options import define, options
import settings



def init_db():
    db_client = None;
    try:
        db_client = asyncmongo.Client(
            pool_id=settings.MONGO_POOL_ID, host=settings.MONGO_HOST, port=settings.MONGO_PORT, 
            maxcached=10, maxconnections=50, dbname=settings.MONGO_DB)
        options.db_client = db_client
        logging.info("Init db successed")
    except Exception,e:
        logging.error("Init db failed",e);

    return db_client