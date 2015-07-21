form models.user import UserModel
import tornado.gen

class OAuthService():
    m_user = UserModel()
    
    def __init__(self):
        pass
      
    @tornado.gen.engine
    def update_gitlab_token(self,user_id,token=None,callback=None):
        user = yield tornado.gen.Task(m_user.update,{"_id":user_id},{"$set":{"gitlab_token":token}})
        callback(user)
