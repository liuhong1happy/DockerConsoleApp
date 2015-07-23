from tornado.auth import OAuth2Mixin,_auth_return_future
from tornado.concurrent import return_future
import settings

class GitLabOAuth2Mixin(OAuth2Mixin):
    _OAUTH_SETTINGS_KEY = 'GITLAB_OAUTH'
    _OAUTH_AUTHORIZE_URL = settings[self._OAUTH_SETTINGS_KEY]['authorize_url']
    _OAUTH_ACCESS_TOKEN_URL = settings[self._OAUTH_SETTINGS_KEY]['access_token_url']
    _OAUTH_USERINFO_URL = settings[self._OAUTH_SETTINGS_KEY]['user_info_url']
    _OAUTH_REDIRECT_URL = settings[self._OAUTH_SETTINGS_KEY]['redirect_url']
    _OAUTH_NO_CALLBACKS = False
    
    @_auth_return_future
    def get_authenticated_user(self, code, callback):
        http = self.get_auth_http_client()
        body = urllib_parse.urlencode({
            "redirect_uri": self._OAUTH_REDIRECT_URL,
            "code": code,
            "client_id": settings[self._OAUTH_SETTINGS_KEY]['key'],
            "client_secret": settings[self._OAUTH_SETTINGS_KEY]['secret'],
            "grant_type": "authorization_code",
        })

        http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
                   functools.partial(self._on_access_token, callback),
                   method="POST", headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=body)

    def _on_access_token(self, future, response):
        if response.error:
            future.set_exception(AuthError('Google auth error: %s' % str(response)))
            return

        args = escape.json_decode(response.body)
        future.set_result(args)
    
    @return_future
    def authorize_redirect(self,extra_params=None,callback=None):
        args = {
            "redirect_uri": self._OAUTH_REDIRECT_URL,
            "client_id": settings[self._OAUTH_SETTINGS_KEY]['key'],
            "response_type": "code"
        }
        self.redirect(url_concat(self._OAUTH_AUTHORIZE_URL, args))
        callback()
        
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
