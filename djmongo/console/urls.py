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

    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/clear$',
         login_required(clear_collection), name="djmongo_clear_collection"), 
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/drop$',
         login_required(delete_collection), name="djmongo_delete_collection"), 

    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/ensure-index$',
         login_required(simple_ensure_index), name="djmongo_simple_index_create"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/delete$',
         login_required(remove_data_from_collection), name="djmongo_remove_data_from_collection_w_params"),
    
    url(r'create-document/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(create_document_in_collection), name="djmongo_create_document_in_collection_w_params"),
    
    url(r'^database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/update$',
        login_required(update_document_in_collection), name="djmongo_update_document_in_collection_w_params"),
    
    url(r'^database/(?P<database_name>[^/]+)/drop$',
         login_required(drop_database), name="djmongo_drop_database"),

    url(r'^database/(?P<database_name>[^/]+)/create-collection$',
         login_required(create_collection), name="djmongo_create_collection"),
    
    #API calls ----------------------------------------------------------------
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/clear$',
         json_login_required(clear_collection), name="djmongo_api_clear_collection"), 
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>[^/]+)/drop$',
         json_login_required(delete_collection), name="djmongo_api_delete_collection"), 
    
    url(r'^api/database/(?P<database_name>[^/]+)/collection/(?P<collection_name>\[^/]+)/ensure-index$',
         json_login_required(csrf_exempt(simple_ensure_index)), name="djmongo_api_simple_index_create"),

    url(r'^api/database/(?P<database_name>[^/]+)/drop$',
         json_login_required(drop_database), name="djmongo_api_drop_database"),

    url(r'^api/database/(?P<database_name>[^/]+)/create-collection$',
         json_login_required(create_collection), name="djmongo_api_create_collection"),    

    )