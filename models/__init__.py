import settings
from tornado.options import define,options
import tornado.gen
import tornado.web
import pymongo
import logging
import time

__all__=["get_list","get_one","update","insert","delete","exsit","count"]

class BaseModel():
    def __init__(self):
        self.db_client = options.db_client;
        self.module = self.__module__
        self.class_name = self.__class__.__name__
        if not hasattr(self, "db"):
            self.db = self.module.split('.')[1]
        if not hasattr(self,"table"):
            self.table = self.class_name
        if not hasattr(self,"key"):
            self.key = "_id"
        self.db_conn  = self.db_client[self.db][self.table]

    @tornado.gen.engine
    def get_list(self,spec,fields=None,sorts=None,skip=0,limit=20,callback=None):
        if(spec==None or not isinstance(spec,dict)):
            spec = {"del_flag":{'$exists': 'False' }}
        else:
            spec["del_flag"] = {'$exists': 'False' }
        if(fields==None or not isinstance(fields,dict)):
            if not hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True,"del_flag":False}
        if(sorts==None or not isinstance(sorts,list)):
            sorts = []
            sorts.append(("_id", pymongo.DESCENDING))
        result = []

        cursor = self.db_conn.find(filter = spec ,projection = fields,sort = sorts,limit = limit,skip = skip)
        
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            result.append(doc)
        callback(result)
    
    @tornado.gen.engine
    def find_one(self,spec_or_id,fields=None,callback=None):
        if(spec_or_id==None):
            callback(None)
        if(isinstance(spec_or_id,dict)):
            spec_or_id["del_flag"] = {'$exists': 'False' }
            
        if(fields==None or not isinstance(fields,dict)):
            if hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True,"del_flag":False}
        result = self.db_conn.find_one(filter = spec_or_id,projection = fields)
        callback(result)
    
    
    @tornado.gen.engine
    def insert_one(self,doc,callback=None):
        create_time = int(time.time())
        if(doc==None):
            callback(None)
        if(isinstance(doc,dict)):
            doc["create_time"] = create_time
            doc["del_flag"] = False
        else:
            callback(None)
        
        result = self.db_conn.insert_one(doc)
        callback(result)
    
    @tornado.gen.engine
    def update(self, spec, document, upsert=False, manipulate=False,
               safe=True, multi=True, callback=None, **kwargs):
        update_time = int(time.time())
        if spec==None or not isinstance(spec,dict):
            spec = {"del_flag":{"$ne":False}}
        elif isinstance(spec,dict):
            spec["del_flag"] = {"$ne":False}
        else:
            callback(None)
        if document==None or not isinstance(spec,dict):
            document = {
                  "$set":{
                    "update_time":update_time
                  }
                }
        elif isinstance(document,dict):
            set_data = document.get("$set",{})
            set_data["update_time"] = update_time
            document["$set"] = set_data
        else:
            callback(None)
            
        result,error = yield tornado.gen.Task(self.db_conn.update,spec,document,upsert=upsert,manipulate=manipulate, safe=safe, multi=multi,**kwargs)
        callback(result)
        
