import tornado.web
from tornado.options import define,options
from tornado import gen
from tornado.concurrent import return_future
from bson.objectid import ObjectId
import settings
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

    @return_future
    def get_list(self,spec,fields=None,sorts=None,skip=0,limit=20,callback=None):
        if(spec is None or not isinstance(spec,dict)):
            spec = {"del_flag":{'$ne': True }}
        else:
            spec["del_flag"] = {'$ne': True }
            spec_id = spec.get("_id",None)
            if spec_id is not None and isinstance(spec_id,str):
                spec["_id"] = ObjectId(spec_id)
        
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
    
    @return_future
    def find_one(self,spec_or_id,fields=None,callback=None):
        if(spec_or_id==None):
            callback(None)
        if(isinstance(spec_or_id,dict)):
            spec_or_id["del_flag"] = {'$ne':True }
            spec_id = spec_or_id.get("_id",None)
            if spec_id is not None and isinstance(spec_id,str):
                spec_or_id["_id"] = ObjectId(spec_id)
        if(isinstance(spec_or_id,str)):
            spec_or_id = ObjectId(spec_or_id)
        if(fields==None or not isinstance(fields,dict)):
            if hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True,"del_flag":False}
        result = self.db_conn.find_one(filter = spec_or_id,projection = fields)
        callback(result)
    
    @return_future
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

    @return_future
    def update_one(self, spec, document, callback=None):
        update_time = int(time.time())
        if spec==None or not isinstance(spec,dict):
            spec = {"del_flag":{"$ne":True}}
        elif isinstance(spec,dict):
            spec["del_flag"] = {"$ne":True}
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
        result =self.db_conn.update_one(spec,document,upsert=False)
        callback(result)
        
