from tornado.options import define,options

class BaseModel():
    def __init__():
        self.db_client = options.db_client;
        if not hasattr(self, "db"):
            self.db = "db_paas"
        if not hasattr(self,"table"):
            self.table = "t_user"
        if not hasattr(self,"key"):
            self.key = "_id"
            
        self.db_conn  = self.db_client.connection(collectionname=self.table, dbname=self.db_client)
        
        
    def get_list(callback):
        self.db_conn.find(callback=callback)
        
         
    
    