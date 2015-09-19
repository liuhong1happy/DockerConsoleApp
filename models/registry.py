from models import BaseModel

class RegistryModel(BaseModel):
    table = "registrys"
    db = "console"
    
    fields={
        "registry_id":True,
        "container_id":True,
        "user_name":True,
        "user_id":True,
        "inspect_container":True,
        "status":True,
        "logs":True,
        "update_time":True,
        'create_time':True
    }