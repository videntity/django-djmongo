#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import write_to_collection

urlpatterns = patterns('',

    
    url(r'^api/(?P<slug>[^/]+)$',
         json_login_required(write_to_collection), name="djmongo_api_write_to_collection"),

    )