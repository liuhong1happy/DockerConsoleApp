from models.container import ContainerModel
import tornado.gen

class ContainerService():
    m_container = ContainerModel()
    
    def insert_image(self,container,callback=None):
        model = yield tornado.gen.Task(m_container.insert,m_container)
        callback(model)
        
    def exist_container(self,service_name,host_ip,callback=None):
        result = yield tornado.gen.Task(m_container.find_one,{"service_name":service_name,"host_ip":host_ip})
        if result==None or not isinstance(result,dict):
            callback(False)
        else:
            callback(True)
    
    def exist_container(self,service_name,host_ip,callback=None):
        result = yield tornado.gen.Task(m_container.find_one,{"service_name":service_name,"host_ip":host_ip})
        if result==None or not isinstance(result,dict):
            callback(None)
        else:
            callback(result)
    
    
    def get_containers(self,spec,fileds=None,sorts=None,page_index=0,page_size=20,callback=None):
        skip = page_index*page_size
        result_list = yield tornado.gen.Task(m_container.find(spec,fields,sorts,skip,page_size)
        if not result_list or len(result_list)==0:
            callback(None)
        else:
            callback(result_list)