#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView
from decorators import json_login_required
from django.contrib.auth.decorators import login_required



urlpatterns = patterns('',


    #API Calls (these return JSON). ------------------------------------------
    url(r'api/test-credentials',  api_test_credentials,
            name='api-test-credentials'),
    url(r'api/user/create',  csrf_exempt(json_login_required(api_user_create)),
        name='djmongo_api_user_create'),
    url(r'api/user/update', api_user_update,  name='djmongo_api_user_update'), 
    url(r'api/user/read/(?P<email>[^/]+)', api_read_user,  name='djmongo_api_read_user'),
    url(r'api/user/delete/(?P<email>[^/]+)', api_delete_user,  name='djmongo_api_delete_user'),
    
    #Web Views that require csrf token -------------------------------
    url(r'user/create',   login_required(user_create),    name='djmongo_user_create'),
    url(r'user/update',   login_required(user_update),    name='djmongo_user_update'),
    url(r'user/password', login_required(user_password),  name='djmongo_user_password'),
    #Login.Logout of the web interface
    url(r'login',  simple_email_login, name='login'),
    url(r'logout', simple_logout,  name='logout'),
    
    
    )