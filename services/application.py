from models.application import ApplicationModel
from tornado import gen

class ApplicationService():
    m_application = ApplicationModel()
    
    @gen.coroutine
    def insert_application(self,application,callback=None):
        project_url = application.get("project_url",None)
        if project_url is None:
            raise gen.Return(None)
        app = yield self.m_application.find_one({"project_url":project_url})
        model = {}
        if app is None:
            model = yield self.m_application.insert_one(application)
            app = yield self.m_application.find_one(model.inserted_id)
        else:
            model = yield self.m_application.update_one({"project_url":project_url},{"$set":application})
        raise gen.Return(application)
    
    @gen.coroutine
    def exist_application(self,project_url,callback=None):
        result = yield self.m_application.find_one({"project_url":project_url})
        if result==None or not isinstance(result,dict):
            raise gen.Return(False)
        else:
            raise gen.Return(True)
    
    @gen.coroutine
    def find_one(self,project_url,callback=None):
        print project_url
        result = yield self.m_application.find_one({"project_url":project_url})
        if result==None or not isinstance(result,dict):
            raise gen.Return(None)
        else:
            raise gen.Return(result)

    @gen.coroutine
    def get_appliactions(self,spec,fields=None,sorts=None,page_index=0,page_size=20,callback=None):
        skip = page_index*page_size
        result_list =yield self.m_application.get_list(spec,fields,sorts,skip,page_size)
        if not result_list or len(result_list)==0:
            raise gen.Return(None)
        else:
            raise gen.Return(result_list)
