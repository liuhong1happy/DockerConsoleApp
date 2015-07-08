from models import BaseModel

class ServiceModel(BaseModel):
    table = "services"
    db = "console"
    
    fields={
        "name":True,
        "user":True,
        "image":True,
        "ports":True,
        "envirements":True,
        "logo":True
    }