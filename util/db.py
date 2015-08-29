import logging 
from tornado.options import define, options
import settings
from pymongo import MongoClient


def init_db():
    db_client = None;
    try:
        uri = 'mongodb://'+settings.MONGO_USER+':'+settings.MONGO_PWD+'@'+settings.MONGO_HOST+':'+str(settings.MONGO_PORT)+'/'+settings.MONGO_DB
        db_client = MongoClient(uri)
        options.db_client = db_client
        logging.info("Init db successed")
    except Exception as e:
        logging.error("Init db failed",e);

    return db_client