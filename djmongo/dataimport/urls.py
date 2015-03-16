#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    url(r'^previous$', login_required(previous_data_imports),
        name="djmongo_previous_data_imports"),
    
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(previous_data_imports),
         name="djmongo_previous_data_imports_w_params"),
    
    url(r'^delete/(?P<slug>\S+)$',
                    login_required(delete_import),
                    name="djmongo_delete_import_by_slug"),
    
    url(r'^csv$', login_required(import_data_file), name="djmongo_import_csv"),
    
    
    url(r'^csv/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(import_data_file), name="djmongo_import_csv_w_params"),
      
    #API calls ----------------------------------------------------------
    url(r'^api/csv$', json_login_required(csrf_exempt(import_data_file)),
        name="djmongo_api_import_data_file"),
    
    url(r'^api/csv/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         json_login_required(csrf_exempt(import_data_file)),
         name="djmongo_api_import_file_w_params"),
    
    )
