from models.registry import RegistryModel
from tornado import gen

class RegistryService():
    m_registry = RegistryModel()
    
    @gen.coroutine
    def insert_registry(self,registry,callback=None):
        registry_id = registry.get("registry_id",None)
        registry = None
        if registry_id is not None:
            registry = yield self.m_registry.find_one(registry_id)
        model = {}
        if registry is None:
            model = yield self.m_registry.insert_one(registry)
            registry = yield self.m_registry.find_one(model.inserted_id)
            registry["_id"] = str(model.inserted_id)
        else:
            model = yield self.m_registry.update_one({ "_id":registry_id},{"$set":registry})
        raise gen.Return(registry)
    
    @gen.coroutine
    def exist_registry(self,registry_id,callback=None):
        result = yield self.m_registry.find_one(registry_id)
        if result==None or not isinstance(result,dict):
            raise gen.Return(False)
        else:
            raise gen.Return(True)
    
    @gen.coroutine
    def find_one(self,registry_id,callback=None):
        result = yield self.m_registry.find_one(registry_id)
        if result==None or not isinstance(result,dict):
            raise gen.Return(None)
        else:
            raise gen.Return(result)