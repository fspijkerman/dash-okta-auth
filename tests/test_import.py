"""
Test Dash Okta Auth.
"""

import pytest

from dash_okta_auth import OktaOAuth

from dash import Dash
from flask import Flask


@pytest.fixture
def app(name='dask'):
    """Dash App."""

    return Dash(name, server=Flask(name),
                url_base_pathname='/', auth='auth')


def test_init(app):
    """Test initialisation."""

    auth = OktaOAuth(app, base_url='https://sbphnk.okta-emea.com')

    assert auth.app is app
