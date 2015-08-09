from models.user  import UserModel
from util.genmd5 import genmd5
from bson.objectid import ObjectId
from tornado import gen
from tornado.concurrent import return_future

class UserService():
    m_user = UserModel()
    @gen.coroutine
    def signup(self,name,email,password,fields=None,callback=None):
        insertData = {
            "name":name,
            "email":email,
            "password":genmd5(password)
        }
        model = yield self.m_user.insert_one(insertData)
        if model is not None:
            result =yield self.m_user.find_one(model.inserted_id ,fields=fields)
            if result is not None:
                result["_id"] = str(result["_id"])
            raise gen.Return(result)
        else:
            raise gen.Return(None)
        
        
    @gen.coroutine
    def find_one(self,spec,fields=None,callback=None):
        result =yield self.m_user.find_one(spec,fields)
        raise gen.Return(result)

    @gen.coroutine
    def signin(self,user_name,user_pwd,fields=None,callback=None):
        result = yield self.m_user.find_one({ "$or":[ {"name":user_name},{"email":user_name }] ,"password": genmd5(user_pwd) },fields)
        raise gen.Return(result)
        
    @gen.coroutine
    def forget(self,email,callback=None):
        result = yield self.m_user.update({"password": genmd5('123456') })
        if result is not None:
            raise gen.Return(True)
        else:
            raise gen.Return(False)
        
    
        
        
    