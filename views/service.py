from services.service import ServiceService
import tornado.web
import tornado.gen
import tornado.escape

class ServiceHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        service_id = self.get_argument("id")
        fields={
            "name":True,
            "user":True,
            "image":True,
            "ports":True,
            "envirements":True,
            "logo":True
        }
        service = tornado.gen.Task(s_service.get_one,service_id,fields=fields)
        
        if not service:
            json = tornado.escape.json_decode({"status":"error","error_code":404})
        else:
            json = tornado.escape.json_decode({"status":"success","data":service})
        self.write(json)
        self.finish()
    
    def post(self):
        git_path = self.get_argument("git_path",None)
        name = self.get_argument("service_name",None)
        user_name = self.get_argument("user_name","admin")
        
        conn = options.mq_connection
        ch = conn.chanel()
        massage = Message({
            code:git_path,
            name:name,
            user:user_name,
            reply:'service_logs'
        })
        ch.exchange_declare(exchange='create_service', type='direct',durable=True)
        self.ch.queue_declare(queue='create_service',durable=True)
        self.ch.queue_bind(queue='create_service',exchange='create_service',routing_key='create_service')
        ch.publish(msg, exchange='create_service', routing_key='create_service')
    
class GetServiceLogsHandler(tornado.web.RequestHandler):
    def get(self):
        service_id = self.get_argument("id")
        fields={
            "logs":True,
            "status":True
        }
        service = tornado.gen.Task(s_service.get_one,service_id,fields=fields)
        
        if not service:
            json = tornado.escape.json_decode({"status":"error","error_code":404})
        else:
            json = tornado.escape.json_decode({"status":"success","data":service})
        self.write(json)
        self.finish()

class GetRunningServiceLogsHandler(tornado.web.RequestHandler):
    def get(self):
        
        
    
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
