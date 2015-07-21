from models.service  import ServiceModel
import tornado.gen

class ServiceService():
    m_service = ServiceModel()
    
    def __init__(self):
        pass
      
    @tornado.gen.engine
    def insert_service(self,service,callback=None):
        model = yield tornado.gen.Task(self.m_service.insert_one,service)
        callback(model)

    @tornado.gen.engine
    def get_list(self,spec,fields=None,sorts=None,page_index=0,page_size=20,callback=None):

        result = yield tornado.gen.Task(self.m_service.get_list,spec,fields=fields,sorts=sorts,skip=page_size*page_index,limit=page_size)
        if result==None or not isinstance(result,list):
            callback(None)
        else:
            callback(result)
