from models import BaseModel

class UserModel(BaseModel):
    table = "users"
    db = "console"
    
    fields = {
        "name":True,
        "email":True,
        "password":True,
        "gitlab_token":True,
        "last_time":True,
        "login_time":True,
        "create_time":True
    }
