from models.registry import RegistryModel
from tornado import gen

class RegistryService():
    m_registry = RegistryModel()
    
    @gen.coroutine
    def insert_registry(self,registry,callback=None):
        user_id = registry.get("user_id",None)
        app = None
        if user_id is not None:
            app = yield self.m_registry.find_one({"user_id":user_id})
        model = {}
        if app is None:
            model = yield self.m_registry.insert_one(registry)
            registry = yield self.m_registry.find_one(model.inserted_id)
            registry["registry_id"] = str(model.inserted_id)
        else:
            model = yield self.m_registry.update_one(str(app["_id"]),{"$set":registry})
            registry["registry_id"] = str(app["_id"])
        raise gen.Return(registry)
    
    @gen.coroutine
    def exist_registry(self,registry_id,callback=None):
        result = yield self.m_registry.find_one(registry_id)
        if result==None or not isinstance(result,dict):
            raise gen.Return(False)
        else:
            raise gen.Return(True)
    
    @gen.coroutine
    def find_one(self,spec_or_id,callback=None):
        result = yield self.m_registry.find_one(spec_or_id)
        if result==None or not isinstance(result,dict):
            raise gen.Return(None)
        else:
            raise gen.Return(result)