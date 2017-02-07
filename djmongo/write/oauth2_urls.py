#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf.urls import url
from .views import write_to_collection_httpauth
from .oauth_views import write_to_collection_oauth2
from .urls import urlpatterns
from apps.dot_ext.decorators import capability_protected_resource

urlpatterns += [

    # Call / Run the write API
    url(r'^api/oauth2/(?P<slug>[^/]+)$',
        capability_protected_resource()(write_to_collection_oauth2),
        name="djmongo_api_write_to_collection_with_oauth2"),
    
]
