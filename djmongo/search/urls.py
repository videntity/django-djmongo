#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    #return JSON

    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
            search_json, name="djmongo_search_json_w_params"),
    
    #return CSV
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
            search_csv, name="djmongo_search_csv_w_params"),
    
    #return HTML Table
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
            search_html, name="djmongo_search_html_w_params"),

   
    url(r'^run-aggregation/(?P<slug>\S+)$',
                    run_aggregation_by_slug,
                    name="djmongo_run_aggregation_by_slug"),
    
    
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
    
    
    url(r'^edit-saved-aggregation/(?P<slug>\S+)$',
                    login_required(edit_saved_aggregation_by_slug),
                    name="djmongo_edit_saved_aggregation_by_slug"),
    
    url(r'^delete-saved-aggregation/(?P<slug>\S+)$',
                    login_required(delete_saved_aggregation_by_slug),
                    name="djmongo_delete_saved_aggregation_by_slug"),
    

    url(r'^create-saved-aggregation/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                   login_required(create_saved_aggregation),
                    name="djmongo_create_saved_aggregation_w_params"),

    
    url(r'^complex-search/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                    login_required(complex_search), name="djmongo_complex_search"),
    


    url(r'^database-access-control/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(database_access_control),
        name="djmongo_database_access_control"),
    
    
    
    url(r'^browse-saved-aggregations/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(display_saved_aggregations),
                name="djmongo_browse_saved_aggregations_w_params"),
    
    
    url(r'^browse-saved-searches/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(display_saved_searches),
                name="djmongo_browse_saved_searches_w_params"),
    
    
    # Unsupported/Experimental
    url(r'^build-keys', login_required(build_keys),
                    name="djmongo_search_build_keys"),
     # Unsupported/Experimental
    url(r'^custom-report', login_required(custom_report),
                   name="cdjmongo_custom_report"),
     # Unsupported/Experimental
    url(r'^data-dictionary', login_required(data_dictionary),
                    name="djmongo_data_dictionary"),
    # Unsupported/Experimental
    url(r'^load-labels-from-data-dictonary',
                    login_required(load_labels),
                    name="djmongo_load_labels"),

    #API CALLS ------------------------------------------------------------------   
    
    #return JSON ----------------------------------------------
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
         search_json, name="djmongo_api_search_json_w_params"),
    
    #return CSV ------------------------------------------------
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
         search_csv, name="djmongo_api_search_csv_w_params"),
 
    #return HTML Table ----------------------------------------------------------  
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
         search_html, name="djmongo_api_search_html_w_params"),
    
    #Saved Search API Calls ------------------------------------------------------- 
    url(r'^api/public/saved-search/(?P<slug>\S+)$',
        run_saved_search_by_slug,
        name="djmongo_api_run_public_saved_search_by_slug"),
    
    url(r'^api/saved-search/(?P<slug>\S+)$',
        json_login_required(run_saved_search_by_slug),
        name="djmongo_api_run_saved_search_by_slug"),
    

    )