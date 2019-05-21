# Dash Okta Auth

Dash Okta Auth is a simple library using Okta OAuth to authenticate and
view a [Dash](https://dash.plot.ly/) app.

This Library uses [Flask Dance](https://github.com/singingwolfboy/flask-dance)
and a modified version of Plotly's own [dash auth](https://github.com/plotly/dash-auth)
for authentication.

This Library is heavily inspired by [dash-google-oauth](https://github.com/lchapo/dash-google-auth) created by Lucas Chapin

## Basic Use

Authentication can be added to your Dash application using the `OktaOAuth`
class, i.e.

```python
from dash import Dash
from flask import Flask
from dash_okta_auth import OktaOAuth

server = Flask(__name__)
server.config.update({
  'OKTA_OAUTH_CLIENT_ID': ...,
  'OKTA_OAUTH_CLIENT_SECRET': ...,
})

app = Dash(__name__, server=server, url_base_pathname='/', auth='auth')

additional_scopes = [...]
auth = OktaOAuth(app, base_url='https://myoktadomain.okta-emea.com', additional_scopes)

# your Dash app here :)
...
```

## Example
Steps to try this out yourself:

1. Install the `dash-okta-auth` library using `pip`:

    ```bash
    $ pip install dash-okta-auth
    ```

2. Follow the [Flask Dance Guide](http://flask-dance.readthedocs.io/en/latest/quickstarts/okta.html)
   to create an app on the okta admin console

3. Make a copy of [app.py](https://github.com/lucaschapin/dash-okta-auth/blob/master/app.py)
   and set the variables (or set the corresponding environment variables):
    ```python
    server.config["OKTA_OAUTH_CLIENT_ID"] = ...
    server.config["OKTA_OAUTH_CLIENT_SECRET"] = ...
    ```
   with values from the Okta OAuth 2 application you should have set up earlier.
   If you've set these up properly, you can find them at
   `Applications > yourapp > General`
   under the section **Client Credentials**.

4. Run `python app.py` and open [localhost](http://localhost:8050/) in a
   browser window to try it out! If the app loads automatically without
   prompting a Okta login, that means you're already authenticated -- try
   using an inokta window in this case if you want to see the login
   experience for a new user.
