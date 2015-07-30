from models.application import ApplicationModel
import tornado.gen

class ApplicationService():
    m_application = ApplicationModel()
    
    @tornado.gen.coroutine
    def insert_application(self,application,callback=None):
        model = self.m_application.insert(application)
        raise tornado.gen.Return(model)
    
    @tornado.gen.coroutine
    def exist_application(self,project_url,callback=None):
        result = self.m_application.find_one({"project_url":project_url})
        if result==None or not isinstance(result,dict):
            raise tornado.gen.Return(False)
        else:
            raise tornado.gen.Return(True)
    
    @tornado.gen.coroutine
    def find_one(self,project_url,callback=None):
        result = self.m_application.find_one({"project_url":project_url})
        if result==None or not isinstance(result,dict):
            raise tornado.gen.Return(None)
        else:
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def get_appliactions(self,spec,fileds=None,sorts=None,page_index=0,page_size=20,callback=None):
        skip = page_index*page_size
        result_list = self.m_application.find(spec,fields,sorts,skip,page_size)
        if not result_list or len(result_list)==0:
            raise tornado.gen.Return(None)
        else:
            raise tornado.gen.Return(result_list)
