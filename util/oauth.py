from tornado.auth import OAuth2Mixin,_auth_return_future,AuthError
from tornado.concurrent import return_future
import settings
import urllib as urllib_parse
from tornado import httpclient,escape
import functools
from tornado.httpclient import AsyncHTTPClient


class GitLabOAuth2Mixin(OAuth2Mixin):

    def __init__(self):
        AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        
    _OAUTH_AUTHORIZE_URL = settings.GITLAB_OAUTH['authorize_url']
    _OAUTH_ACCESS_TOKEN_URL = settings.GITLAB_OAUTH['access_token_url']
    _OAUTH_USERINFO_URL = settings.GITLAB_OAUTH['user_info_url']
    _OAUTH_REDIRECT_URL = settings.GITLAB_OAUTH['redirect_url']
    _OAUTH_NO_CALLBACKS = False
    
    @_auth_return_future
    def get_authenticated_user(self, code, callback):
        http = self.get_auth_http_client()
        body = urllib_parse.urlencode({
            "redirect_uri": self._OAUTH_REDIRECT_URL,
            "code": code,
            "client_id": settings.GITLAB_OAUTH['key'],
            "client_secret": settings.GITLAB_OAUTH['secret'],
            "grant_type": "authorization_code",
        })
        
        http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
                   functools.partial(self._on_access_token, callback),
                   method="POST", headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=body)
        
    def _on_oauth2_request(self, future, response):
        if response.error:
            future.set_exception(AuthError("Error response %s fetching %s" %
                                           (response.error, response.request.url)))
            return
        future.set_result(escape.json_decode(response.body))
        
        
        
    def _on_access_token(self, future, response):
        if response.error:
            future.set_exception(AuthError('Gitlab auth error: %s' % str(response)))
            return

        args = escape.json_decode(response.body)
        future.set_result(args)
    
    @return_future
    def authorize_redirect(self,extra_params=None,callback=None):
        args = {
            "redirect_uri": self._OAUTH_REDIRECT_URL,
            "client_id": settings.GITLAB_OAUTH['key'],
            "response_type": "code"
        }
        self.redirect(url_concat(self._OAUTH_AUTHORIZE_URL, args))
        callback()

    @_auth_return_future
    def get_by_api(self, api, callback=None, access_token=None,post_args=None, **kwargs):
        url = settings.GITLAB_SITE_URL+api
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
        if all_args:
            url += "?" + urllib_parse.urlencode(all_args)
        
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url,functools.partial(self._on_oauth2_request, callback), method="POST", body=urllib_parse.urlencode(post_args),**kwargs)
        else:
            http.fetch(url, functools.partial(self._on_oauth2_request, callback),**kwargs)
    
    @_auth_return_future
    def get_user_info(self,callback,access_token=None,post_args=None, **args):
        url = self._OAUTH_USERINFO_URL
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)

        if all_args:
            url += "?" + urllib_parse.urlencode(all_args)
        callback = functools.partial(self._on_oauth2_request, callback)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)
    

    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()