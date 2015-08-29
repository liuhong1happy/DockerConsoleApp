from models import BaseModel

class ApplicationModel(BaseModel):
    table = "applications"
    db = "console"
    
    fields={
        "application_id":True,
        "container_id":True,
        "project_url":True,
        "project_name":True,
        "storage_path":True,
        "app_name":True,
        "run_host":True,
        "user_id":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }