#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf.urls import url
from .urls import urlpatterns
from apps.dot_ext.decorators import capability_protected_resource
from oauth2_provider.decorators import protected_resource
from .views.run import simple_search, run_custom_public_read_api_by_slug

urlpatterns += [

    url(r'^api/oauth2/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        capability_protected_resource()(simple_search), name="djmongo_api_oauth2_simple_search"),

    url(r'^api/custom/oauth2/(?P<slug>\S+)$',
        capability_protected_resource()(run_custom_public_read_api_by_slug),
        name="djmongo_run_custom_oauth2_read_api_by_slug"),

]
