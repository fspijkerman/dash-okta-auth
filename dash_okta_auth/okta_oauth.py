from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError, OAuth2Error
from flask import (
    redirect,
    url_for,
    Response,
    abort,
    session,
)
from flask_dance.contrib.okta import (
  make_okta_blueprint,
  okta
)

from .auth import Auth

class OktaOAuth(Auth):
    def __init__(self, app, base_url, additional_scopes=None):
        super(OktaOAuth, self).__init__(app)
        okta_bp = make_okta_blueprint(
            base_url=base_url,
            authorization_url=base_url + '/oauth2/default/v1/authorize',
            token_url=base_url + '/oauth2/default/v1/token', 
            scope=[
                "openid",
                "email",
                "profile",
            ] + (additional_scopes if additional_scopes else [])
        )
        app.server.register_blueprint(okta_bp, url_prefix="/login")

    def is_authorized(self):
        if not okta.authorized:
            # send to okta login
            return False

        try:
            resp = okta.get("/oauth2/default/v1/userinfo")
            assert resp.ok, resp.text

            session['email'] = resp.json().get('email')
            return True
        except (InvalidGrantError, TokenExpiredError):
            return self.login_request()

    def login_request(self):
        # send to okta auth page
        return redirect(url_for("okta.login"))

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()
        return wrap
