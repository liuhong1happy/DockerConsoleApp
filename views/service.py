from services.service import ServiceService
import tornado.web
import tornado.gen
import tornado.escape

class ServiceHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")
        self.finish()

class ServicesHandler(tornado.web.RequestHandler):
    s_service = ServiceService()
    
    @tornado.web.asynchronous
    def get(self):
        spec_type = self.get_argument("spec_type","name")
        spec_text =  self.get_argument("spec_text","")
        page_index = self.get_argument("page_index",0)
        page_size = self.get_argument("page_size",20)
        spec ={}
        spec[spec_type]=spec_text
        fields={
            "name":True,
            "user":True,
            "image":True,
            "ports":True,
            "envirements":True,
            "logo":True
        }
        services = tornado.gen.Task(s_service.get_list,spec,fields=fields,page_index=page_index,page_size=page_size)
        json = {}
        if not services:
            json = tornado.escape.json_decode({"status":"error","error_code":404})
        else:
            json = tornado.escape.json_decode({"status":"success","data":services})
        self.write(json)
        self.finish()
