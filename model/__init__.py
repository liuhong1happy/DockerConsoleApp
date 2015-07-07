from tornado.options import define,options
import tornado.gen
import pymongo

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
        
        
    def get_list(spec=None,fileds=None,sorts=None,skip=0,limit=20,callback):
        if(spec==None or isinstance(spec,dict)):
            spec = {}
        if(fields==None or isinstance(fields,dict)):
            if not hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True}
        if(sorts==None or isinstance(sorts,list):
            sorts = []
            sorts.append(["_id", pymongo.DESCENDING])
        result_list,error = yield tornado.gen.Task( self.db_conn.find,
            spec = spec,fields = fields,
            sort = sorts,limit = limit,skip = skip
        )
        callback(result_list)
    
    def get_one(spec_or_id,fields,callback):
        if(fields==None or isinstance(fields,dict)):
            if not hasattr(self,"fields"):
                fields = self.fields
            else:
                fields = {"_id":True}
        result,error = yield tornado.gen.Task( self.db_conn.find_one,spec,fields = fields)
        callback(result)
         
    
    
