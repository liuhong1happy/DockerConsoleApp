#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services.oauth import OAuthService
import tornado.web
import tornado.gen
import settings
from views import BaseHandler,AsyncBaseHandler
from util.oauth import GitLabOAuth2Mixin

class GitLabOAuthHandler(BaseHandler,GitLabOAuth2Mixin):
    s_oauth = OAuthService()
    
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument('code', False)
        if code:
            access = yield self.get_authenticated_user(code=code)
            user_info = yield self.get_user_info(access_token=access["access_token"])
            groups_info = yield self.get_by_api("/api/v3//groups",access_token=access["access_token"])
            for i in range(len(groups_info)):
                group_info = yield self.get_by_api("/api/v3/groups/"+str(groups_info[i]["id"]),access_token=access["access_token"])
                groups_info[i]["details"] = group_info
            user_id = self.current_user["_id"]
            user = yield self.s_oauth.update_gitlab_token(user_id,{"result_code":code,"access_token":access,"user_info":user_info})
        else:
            yield self.authorize_redirect()

class GitLabTokenHandler(AsyncBaseHandler):
    s_oauth = OAuthService()
    @tornado.gen.coroutine
    def _get_(self):
        user_id = self.current_user["_id"]
        token = yield self.s_oauth.get_gitlab_token(user_id)
        if token is None:
            self.render_error(error_code=404,msg="not find data")
        else:
            print token
            self.write_result(data=token)
        