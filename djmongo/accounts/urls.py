#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls import url
from .views import (api_test_credentials, simple_logout, simple_login,
                    user_password, api_user_create, api_read_user,
                    api_delete_user, api_user_update, user_create,
                    user_update)
from .decorators import json_login_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # API Calls (these return JSON). ------------------------------------------
    url(r'api/test-credentials', api_test_credentials,
        name='api-test-credentials'),
    url(r'api/user/create', csrf_exempt(json_login_required(api_user_create)),
        name='djmongo_api_user_create'),
    url(r'api/user/update', api_user_update, name='djmongo_api_user_update'),
    url(r'api/user/read/(?P<email>[^/]+)',
        api_read_user, name='djmongo_api_read_user'),
    url(r'api/user/delete/(?P<email>[^/]+)',
        api_delete_user,
        name='djmongo_api_delete_user'),

    # Web Views that require csrf token -------------------------------
    url(r'user/create', login_required(user_create),
        name='djmongo_user_create'),
    url(r'user/update', login_required(user_update),
        name='djmongo_user_update'),
    url(r'user/password',
        login_required(user_password),
        name='djmongo_user_password'),
    # Login.Logout of the web interface
    url(r'^logout$', simple_logout, name="djmongo_logout"),
    url(r'^login$', simple_login, name="djmongo_login"),
]
