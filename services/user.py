from models.user  import UserModel
import tornado.gen
from util.genmd5 import genmd5
from bson.objectid import ObjectId

class UserService():
    m_user = UserModel()
    @tornado.gen.engine
    def signup(self,name,email,password,fields=None,callback=None):
        insertData = {
            "name":name,
            "email":email,
            "password":genmd5(password)
        }
        model = yield tornado.gen.Task(self.m_user.insert_one,insertData)
        if model is not None:
            result =yield tornado.gen.Task(self.m_user.find_one, model.inserted_id ,fields=fields)
            if result is not None:
                result["_id"] = str(result["_id"])
            callback(result)
        else:
            callback(None)
        
        
    @tornado.gen.engine
    def find_one(self,spec,fields=None,callback=None):
        result =yield  tornado.gen.Task(self.m_user.find_one,spec,fields)
        callback(result)

    @tornado.gen.engine
    def signin(self,user_name,user_pwd,fields=None,callback=None):
        result = yield tornado.gen.Task(self.m_user.find_one,
            { "$or":[ {"name":user_name},{"email":user_name }] ,"password": genmd5(user_pwd) },fields)
        callback(result)
        
    @tornado.gen.engine
    def forget(self,email,callback=None):
        result = yield tornado.gen.Task(self.m_user.update,{"password": genmd5('123456') })
        if result is not None:
            callback(True)
        else:
            callback(False)
        
    
        
        
    