#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',

    url(r'^$', login_required(showdbs), name="djmongo_show_dbs"),
    
    url(r'^new-database$', create_new_database, name="djmongo_create_new_database"),

    url(r'^logout$', simple_logout, name="djmongo_logout"),
    url(r'^login$', simple_login, name="djmongo_login"),

    url(r'^clear-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(clear_collection),
         name="djmongo_clear_collection"), 
    
    url(r'^drop-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)',
         login_required(drop_collection), name="djmongo_drop_collection"), 

    url(r'^ensure-index/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(simple_ensure_index), name="djmongo_ensure_index"),
    
    url(r'^clear-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(remove_data_from_collection),
         name="djmongo_remove_data_from_collection_w_params"),
    
    url(r'create-document/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(create_document_in_collection),
         name="djmongo_create_document_in_collection_w_params"),
    
    url(r'^update-document/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(update_document_in_collection),
        name="djmongo_update_document_in_collection_w_params"),
    
    
    url(r'^drop-database/(?P<database_name>[^/]+)$',
         login_required(drop_database), name="djmongo_drop_database"),

    url(r'^create-collection/(?P<database_name>[^/]+)$',
         login_required(create_collection), name="djmongo_create_collection"),
    
    #API calls ----------------------------------------------------------------
    url(r'^api/clear-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         json_login_required(clear_collection),
            name="djmongo_api_clear_collection"), 
    
    url(r'^api/drop-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         json_login_required(drop_collection),
            name="djmongo_api_delete_collection"), 
    
    url(r'^api/ensure-index/(?P<database_name>[^/]+)/(?P<collection_name>\[^/]+)$',
         json_login_required(csrf_exempt(simple_ensure_index)),
            name="djmongo_api_djmongo_ensure_indexe"),

    url(r'^api/drop-database/(?P<database_name>[^/]+)$',
         json_login_required(drop_database), name="djmongo_api_drop_database"),

    url(r'^api/create-collection/(?P<database_name>[^/]+)$',
         json_login_required(create_collection), name="djmongo_api_create_collection"),    

    )