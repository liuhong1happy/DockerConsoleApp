from models.user import UserModel
from tornado import gen
from tornado.concurrent import return_future


class OAuthService():
    m_user = UserModel()
    
    def __init__(self):
        pass
      
    @gen.coroutine
    def update_gitlab_token(self,user_id,token=None,callback=None):
        one = yield self.m_user.find_one(user_id)
        user = yield self.m_user.update_one({"_id":user_id},{"$set":{"gitlab_token":token}})
        raise gen.Return(user)
    
    @gen.coroutine
    def get_gitlab_token(self,user_id,callback=None):
        user = yield self.m_user.find_one(user_id)
        
        if user is None:
            raise gen.Return(None)
        else:
            gitlab_token = user.get("gitlab_token",False)
            if  gitlab_token:
                raise gen.Return(gitlab_token)
            else:
                raise gen.Return(None)