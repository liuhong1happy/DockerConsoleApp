from models.user import UserModel
import tornado.gen

class OAuthService():
    m_user = UserModel()
    
    def __init__(self):
        pass
      
    @tornado.gen.engine
    def update_gitlab_token(self,user_id,token=None,callback=None):
        user = yield tornado.gen.Task(self.m_user.update,{"_id":user_id},{"$set":{"gitlab_token":token}})
        callback(user)
    
    @tornado.gen.engine
    def get_gitlab_token(self,user_id,callback=None):
        user = yield tornado.gen.Task(self.m_user.find_one,user_id)
        if user is None:
            callback(None)
        else:
            if  hasattr(user,'gitlab_token'):
                callback(user["gitlab_token"])
            else:
                callback(None)