from models.application_access import ApplicationAccessModel
from tornado import gen

class ApplicationAccessService():
    m_application_access = ApplicationAccessModel()
    
    @gen.coroutine
    def access_application(self,access,callback=None):
        print "ccc"
        print access
        access_id = access.get("access_id",None)
        model = {}
        id = ""
        if access_id is None:
            model = yield self.m_application_access.insert_one(access)
            access_id = str(model.inserted_id)
        else:
            model = yield self.m_application_access.update_one({"_id":access_id},{"$set":access})
        raise gen.Return(access_id)
    
    @gen.coroutine
    def exist_access(self,access_id,callback=None):
        result = yield self.m_application_access.find_one(access_id)
        if result==None or not isinstance(result,dict):
            raise gen.Return(False)
        else:
            raise gen.Return(True)
    
    @gen.coroutine
    def find_one(self,access_id,callback=None):
        result = yield self.m_application_access.find_one(access_id)
        if result==None or not isinstance(result,dict):
            raise gen.Return(None)
        else:
            raise gen.Return(result)

    @gen.coroutine
    def get_container_access(self,container_id,fields=None,sorts=None,page_index=0,page_size=20,callback=None):
        skip = page_index*page_size
        result_list =yield self.m_application_access.get_list({"container_id":container_id },fields,sorts,skip,page_size)
        if not result_list or len(result_list)==0:
            raise gen.Return(None)
        else:
            raise gen.Return(result_list)
