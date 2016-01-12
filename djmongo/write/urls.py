#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',

    
    url(r'^api/(?P<slug>[^/]+)$',
         write_to_collection_httpauth, name="djmongo_api_write_to_collection"),

    url(r'^api/ip/(?P<slug>[^/]+)$',
         write_to_collection_ip_auth, name="djmongo_api_write_to_collection_with_ip"),
    
    url(r'^browse-ip-write-apis/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(browse_ip_write_apis),
                name="djmongo_browse_ip_write_apis_w_params"),
  
    url(r'^browse-httpauth-write-apis/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(browse_httpauth_write_apis),
                name="djmongo_browse_httpauth_write_apis_w_params"),
    
    url(r'^browse-ip-write-apis$',
                login_required(browse_ip_write_apis),
                name="djmongo_browse_ip_write_apis"),
  
    url(r'^browse-httpauth-write-apis$',
                login_required(browse_httpauth_write_apis),
                name="djmongo_browse_httpauth_write_apis"),

    )