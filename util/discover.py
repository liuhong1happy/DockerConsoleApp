import logging 
import etcd
from tornado.options import define, options
import settings



def init_etcd():
    etcd_client = None
    try:
        etcd_client = etcd.Client(settings.ETCD_HOST,settings.ETCD_PORT)
        options.etcd_client = etcd_client
        logging.info("Init etcd successed")
    except Exception,e:
        logging.error("Init etcd failed",e)

    return etcd_client