from tornado.options import define,options
import tornado.gen
import pymongo
import logging
import time

__all__=["get_list","get_one","update","insert","delete","exsit","count"]

class BaseModel():
    def __init__():
        self.db_client = options.db_client;
        self.module = self.__module__
        self.class_name = self.__class__.__name__
        if not hasattr(self, "db"):
            self.db = self.module.split('.')[1]
        if not hasattr(self,"table"):
            self.table = self.class_name
        if not hasattr(self,"key"):
            self.key = self.class_name+"_id"
        

        self.db_conn  = self.db_client.connection(collectionname=self.table, dbname=self.db_client)
        
        
    def get_list(spec,fileds=None,sorts=None,skip=0,limit=20,callback=None):
        if(spec==None or not isinstance(spec,dict)):
            spec = {"del_flag":False}
        else:
            spec["del_flag"] = False
        if(fields==None or not isinstance(fields,dict)):
            if not hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True,"del_flag":False}
        if(sorts==None or not isinstance(sorts,list):
            sorts = []
            sorts.append(["_id", pymongo.DESCENDING])
        result_list,error = yield tornado.gen.Task( self.db_conn.find,
            spec = spec,fields = fields,
            sort = sorts,limit = limit,skip = skip
        )
        callback(result_list)
    
    def get_one(spec_or_id,fields=None,callback=None):
        if(spec_or_id==None):
            callback(None)
        if(isinstance(spec_or_id,dict):
            spec_or_id["del_flag"] = False 
        
        if(fields==None or not isinstance(fields,dict)):
            if not hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True}
        result,error = yield tornado.gen.Task(self.db_conn.find_one,spec_or_id,fields = fields)
        callback(result)
    
    def insert(self,doc_or_docs,manipulate=True, safe=True, check_keys=True, callback=None,**kwargs):
        create_time = int(time.time())
        if(doc_or_docs==None):
            callback(None)
        if(isinstance(doc_or_docs,dict)):
            doc_or_docs["create_time"] = create_time
            doc_or_docs["del_flag"] = False
        elif(isinstance(doc_or_docs,list)):
            for doc in doc_or_docs:
                doc["create_time"] = create_time
                doc["del_flag"] = False
        else:
            callback(None)
            
        result,error = yield tornado.gen.Task(self.db_conn.insert,doc_or_docs,manipulate=manipulate, safe=safe, check_keys=check_keys,**kwargs)
        callback(result)
    
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
        
