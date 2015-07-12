from models import BaseModel

class ServiceModel(BaseModel):
    table = "services"
    db = "console"
    
    fields={
        "name":True,
        "user":True,
        "code":True,
        "logs":True
    }