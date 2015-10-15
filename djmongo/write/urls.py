#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import patterns, include, url
from views import write_to_collection_httpauth, write_to_collection_ip_auth

urlpatterns = patterns('',

    
    url(r'^api/(?P<slug>[^/]+)$',
         write_to_collection_httpauth, name="djmongo_api_write_to_collection"),

    url(r'^api/ip/(?P<slug>[^/]+)$',
         write_to_collection_ip_auth, name="djmongo_api_write_to_collection_with_ip"),
    )