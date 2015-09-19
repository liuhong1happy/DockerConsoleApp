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
        pass

    # 开启加速器
    @gen.coroutine
    def _post(self):
        pass