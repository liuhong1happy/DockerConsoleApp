from tornado.auth import OAuth2Mixin,_auth_return_future
import settings

class GitLabOAuth2Mixin(OAuth2Mixin):
    _OAUTH_SETTINGS_KEY = 'GITLAB_OAUTH'
    _OAUTH_AUTHORIZE_URL = settings[self._OAUTH_SETTINGS_KEY]['authorize_url']
    _OAUTH_ACCESS_TOKEN_URL = settings[self._OAUTH_SETTINGS_KEY]['access_token_url']
    _OAUTH_USERINFO_URL = settings[self._OAUTH_SETTINGS_KEY]['user_info_url']
    _OAUTH_NO_CALLBACKS = False
    
    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, code, callback):
        http = self.get_auth_http_client()
        body = urllib_parse.urlencode({
            "redirect_uri": redirect_uri,
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
