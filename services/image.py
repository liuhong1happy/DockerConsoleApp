from models.image  import ImageModel
import tornado.gen

class ImageService():
    m_image = ImageModel()
    
    def insert_image(self,image,callback=None):
        model = yield tornado.gen.Task(m_image.insert,image)
        callback(model)
        
    def exist_image(self,user_name,service_name,callback=None):
        result = yield tornado.gen.Task(m_image.find_one,{"user_name":user_name,"service_name":service_name})
        if result==None or not isinstance(result,dict):
            callback(False)
        else:
            callback(True)
    
    def get_image(self,image_id,callback=None):
        result = yield tornado.gen.Task(m_user.find_one,{"_id":image_id})
        if result==None or not isinstance(result,dict):
            callback(None)
        else:
            callback(result)
    
    
    def get_images(self,spec,fileds=None,sorts=None,page_index=0,page_size=20,callback=None):
        skip = page_index*page_size
        result_list = yield tornado.gen.Task(m_image.find(spec,fields,sorts,skip,page_size)
        if not result_list or len(result_list)==0:
            callback(None)
        else:
            callback(result_list)