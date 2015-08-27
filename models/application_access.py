from models import BaseModel

class ApplicationAccessModel(BaseModel):
    table = "applications_access"
    db = "console"
    
    fields={
        "access_type":True,
        "access_content":True,
        "container_id":True,
        "container_host":True,
        "container_name":True,
        "user_id":True,
        "response":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }