from models.service  import ServiceModel
from tornado import gen

class ServiceService():
    m_service = ServiceModel()
    
    def __init__(self):
        pass
      
    @gen.coroutine
    def insert_service(self,service,callback=None):
        model = yield self.m_service.insert_one(service)
        raise gen.Return(model)

    @gen.coroutine
    def get_list(self,spec,fields=None,sorts=None,page_index=0,page_size=20,callback=None):
        result = yield self.m_service.get_list(spec,fields=fields,sorts=sorts,skip=page_size*page_index,limit=page_size)
        if result==None or not isinstance(result,list):
            raise gen.Return(None)
        else:
            raise gen.Return(result)
