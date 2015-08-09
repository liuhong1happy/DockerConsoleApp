from models import BaseModel

class ApplicationModel(BaseModel):
    table = "applications"
    db = "console"
    
    fields={
        "project_url":True,
        "project_name":True,
        "storage_path":True,
        "app_name":True,
        "user_id":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }