#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.conf.urls import include, url
from .views import *


urlpatterns = [  
   
    url(r'^run-aggregation/(?P<slug>\S+)$',
                    run_aggregation_by_slug,
                    name="djmongo_run_aggregation_by_slug"),
    
    url(r'^edit-saved-aggregation/(?P<slug>\S+)$',
                    login_required(edit_saved_aggregation_by_slug),
                    name="djmongo_edit_saved_aggregation_by_slug"),
    
    url(r'^delete-saved-aggregation/(?P<slug>\S+)$',
                    login_required(delete_saved_aggregation_by_slug),
                    name="djmongo_delete_saved_aggregation_by_slug"),
    
    url(r'^browse-saved-aggregations/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(browse_saved_aggregations),
                name="djmongo_browse_saved_aggregations_w_params"),
    
    url(r'^create-saved-aggregation/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                   login_required(create_saved_aggregation),
                    name="djmongo_create_saved_aggregation_w_params"),
]