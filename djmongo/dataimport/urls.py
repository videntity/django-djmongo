#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    url(r'^previous$', login_required(previous_data_imports),
        name="previous_data_imports"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/previous$',
         login_required(previous_data_imports),
         name="previous_data_imports_w_params"),
    
    url(r'^delete/(?P<slug>\S+)$',
                    login_required(delete_import),
                    name="delete_import_by_slug"),
    
    url(r'^file$', login_required(import_data_file), name="import_data_file"),
    
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/file$',
         login_required(import_data_file), name="import_file_w_params"),
      
    #API calls ----------------------------------------------------------
    url(r'^api/file$', json_login_required(csrf_exempt(import_data_file)),
        name="api_import_data_file"),
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/file$',
         json_login_required(csrf_exempt(import_data_file)),
         name="api_import_file_w_params"),
    
    )
