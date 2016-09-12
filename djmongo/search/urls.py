#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import include, url
from .views import *


urlpatterns = [  

       
    url(r'^saved-search/(?P<slug>\S+)$',
                    login_required(run_saved_search_by_slug),
                    name="djmongo_run_saved_search_by_slug"),
    
    url(r'^public/saved-search/(?P<slug>\S+)$',
                    run_saved_search_by_slug,
                    name="djmongo_run_public_saved_search_by_slug"),
   
    url(r'^edit-saved-search/(?P<slug>\S+)$',
                    login_required(edit_saved_search_by_slug),
                    name="djmongo_edit_saved_search_by_slug"),
    
    url(r'^delete-saved-search/(?P<slug>\S+)$',
                    login_required(delete_saved_search_by_slug),
                    name="djmongo_delete_saved_search_by_slug"),
    
    url(r'^create-saved-search/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                    login_required(create_saved_search),
                    name="djmongo_create_saved_search_w_params"),
    

    url(r'^database-access-control/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(database_access_control),
        name="djmongo_database_access_control"),
    

    
    url(r'^browse-saved-searches/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(browse_saved_searches),
                name="djmongo_browse_saved_searches_w_params"),
    
    # Unsupported/Experimental
    url(r'^build-keys/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                    login_required(build_keys),
                    name="djmongo_build_keys"),


    #API CALLS ------------------------------------------------------------------
   
    #return JSON ----------------------------------------------------------------
    
    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
        search_json, name="djmongo_api_search_json_w_params"),
    
    #return CSV ----------------------------------------------------------------
    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
        search_csv, name="djmongo_api_search_csv_w_params"),
 
    #return HTML Table ----------------------------------------------------------  
    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
        search_html, name="djmongo_api_search_html_w_params"),
   
   
    #return JSON ----------------------------------------------
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
         json_login_required(search_json), name="djmongo_api_search_json_w_params"),
    
    #return CSV ------------------------------------------------
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
         json_login_required(search_csv), name="djmongo_api_search_csv_w_params"),
 
    #return HTML Table ----------------------------------------------------------  
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
          json_login_required(search_html), name="djmongo_api_search_html_w_params"),
    
    #Saved Search API Calls ------------------------------------------------------- 
    url(r'^api/public/saved-search/(?P<slug>\S+)$',
        run_saved_search_by_slug,
        name="djmongo_api_run_public_saved_search_by_slug"),
    
    url(r'^api/saved-search/(?P<slug>\S+)$',
        json_login_required(run_saved_search_by_slug),
        name="djmongo_api_run_saved_search_by_slug"),
    

    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
            search_json, name="djmongo_search_json_w_params"),
    
    #return CSV
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
            search_csv, name="djmongo_search_csv_w_params"),
    
    #return HTML Table
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
            search_html, name="djmongo_search_html_w_params"),


    ]