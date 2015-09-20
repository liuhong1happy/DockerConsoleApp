#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.registry import RegistryService
import tornado.web
from tornado import gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings
from views import AsyncBaseHandler

class RegistryHandler(AsyncBaseHandler):
    s_registry = RegistryService()
    # 获取是否存在加速器
    @gen.coroutine
    def _get_(self):
        user_id = str(self.current_user.get("_id",None))
        registry = yield self.s_registry.find_one({"user_id":user_id})
        self.write_result(data=registry)

    # 开启加速器
    @gen.coroutine
    def _post_(self):
        user_id = str(self.current_user.get("_id",None))
        user_name = str(self.current_user.get("name",None))
        import time
        create_time = time.time()
        # 数据库操作
        insertData = {}
        insertData["user_id"] = user_id
        insertData["status"] = 'start'
        insertData["logs"] = [{"create_time":create_time,"info":{"stream":"started user registry"},"user_id":user_id}]
        result = yield self.s_registry.insert_registry(insertData)
        # 加入队列
        msg = Message( json.dumps({
            "registry_id":result["registry_id"],
            "user_id":user_id,
            "user_name":user_name
        }))
        send_message(msg,settings.RUN_REGISTRY_EXCHANGE,settings.RUN_REGISTRY_ROUTING)
        if result is None:
            self.render_error(error_code=404,msg="not data")
        else:
            insertData["_id"] = result["registry_id"]
            self.write_result(data=insertData)