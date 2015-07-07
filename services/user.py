from models.user  import UserModel
import tornado.gen

class UserService():
    m_user = UserModel()
    
    def insert_user(self,user,callback=None):
        model = yield tornado.gen.Task(m_user.insert,user)
        callback(model)
        
    def exist_user(self,user_name,user_pwd,callback=None):
        result = yield tornado.gen.Task(m_user.find_one,{"name":user_name,"pwd":user_pwd})
        if result==None or not isinstance(result,dict):
            callback(False)
        else:
            callback(True)
    
    def get_user(self,user_name,user_pwd,callback=None):
        result = yield tornado.gen.Task(m_user.find_one,{"name":user_name,"pwd":user_pwd})
        if result==None or not isinstance(result,dict):
            callback(None)
        else:
            callback(result)
        
    
        
        
    