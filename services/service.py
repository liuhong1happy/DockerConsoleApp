from models.service  import ServiceModel
from tornado import gen

class ServiceService():
    m_service = ServiceModel()
    
    def __init__(self):
        pass
      
    @gen.coroutine
    def insert_service(self,service,callback=None):
        project_url = service.get("project_url",None)
        if project_url is None:
            raise gen.Return(None)
        project = yield self.m_service.find_one({"project_url":project_url})
        model = {}
        if project is None:
            model = yield self.m_service.insert_one(service)
            project = yield self.m_service.find_one(model.inserted_id)
        else:
            model = yield self.m_service.update_one({"project_url":project_url},{"$set":service})
        raise gen.Return(project)

    @gen.coroutine
    def get_list(self,spec,fields=None,sorts=None,page_index=0,page_size=20,callback=None):
        result = yield self.m_service.get_list(spec,fields=fields,sorts=sorts,skip=page_size*page_index,limit=page_size)
        if result==None or not isinstance(result,list):
            raise gen.Return(None)
        else:
            raise gen.Return(result)

    @gen.coroutine
    def find_one(self,spec_or_id,fields=None,callback=None):
        result = yield self.m_service.find_one(spec_or_id,fields=fields)
        raise gen.Return(result) 