from models import BaseModel

class ServiceModel(BaseModel):
    table = "services"
    db = "console"
    
    fields={
        "project_url":True,
        "project_name":True,
        "project_id":True,
        "user_id":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }
