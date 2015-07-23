#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.oauth import OAuthService
import tornado.web
import tornado.gen
import tornado.escape
import json
from util.rabbitmq import send_message
from stormed import Message
import settings
from views import AsyncBaseHandler
from util.oauth import GitLabOAuth2Mixin

class GitLabOAuthHandler(AsyncBaseHandler,GitLabOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(code=self.get_argument('code'))
            user = yield self.get_user_info(access_token=access["access_token"])
            # Save the user and access token with
            # e.g. set_secure_cookie.
        else:
            yield self.authorize_redirect()

