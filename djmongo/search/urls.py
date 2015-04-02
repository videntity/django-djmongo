#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required
from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    #return JSON

    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/search.json$',
            search_json, name="djmongo_search_json_w_params"),
    
    #return CSV
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/search.csv$',
            search_csv, name="djmongo_search_csv_w_params"),
    
    #return HTML Table
    url(r'^(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/search.html$',
            search_html, name="djmongo_search_html_w_params"),

    url(r'^run-private-saved-search/(?P<slug>\S+)/(?P<skip>[^/]+)/(?P<limit>[^/]+)$',
                    login_required(run_saved_search_by_slug),
                    name="djmongo_run_saved_search_by_slug"),


    url(r'^run-public-saved-search/(?P<slug>\S+)/(?P<skip>[^/]+)/(?P<limit>[^/]+)$',
                    run_saved_search_by_slug,
                    name="djmongo_run_saved_search_by_slug"),
    
    url(r'^run/(?P<slug>\S+)$',
                    login_required(run_saved_search_by_slug),
                    name="djmongo_run_saved_search_by_slug"),
    
    url(r'^run-public/(?P<slug>\S+)$',
                    run_saved_search_by_slug,
                    name="djmongo_run_saved_search_by_slug"),
   
    url(r'^edit-saved-search/(?P<slug>\S+)$',
                    login_required(edit_saved_search_by_slug),
                    name="djmongo_edit_saved_search_by_slug"),
    
    url(r'^delete-saved-search/(?P<slug>\S+)$',
                    login_required(delete_saved_search_by_slug),
                    name="djmongo_delete_saved_search_by_slug"),
    
    url(r'^create-saved-search$', login_required(create_saved_search),
                    name="djmongo_create_saved_search"),

    
    
    url(r'^create-saved-search/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(create_saved_search), name="djmongo_create_saved_search_w_params"),


    url(r'^create-saved-aggregation/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                   login_required(create_saved_aggregation),
                    name="djmongo_create_saved_aggregation_w_params"),

    
    url(r'^complex-search/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
         login_required(complex_search), name="djmongo_complex_search"),
    
    url(r'^browse-saved-searches$', login_required(display_saved_searches),
                    name="djmongo_browse_saved_searches"),
    
    url(r'^browse-saved-searches/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
                login_required(display_saved_searches),
                    name="djmongo_browse_saved_searches_w_params"),
    
    url(r'^build-keys', login_required(build_keys),
                    name="djmongo_search_build_keys"),
    
    url(r'^custom-report', login_required(custom_report),
                   name="cdjmongo_ustom_report"),
    
    url(r'^data-dictionary', login_required(data_dictionary),
                    name="djmongo_data_dictionary"),
    
    url(r'^load-labels-from-data-dictonary', login_required(load_labels),
                    name="djmongo_load_labels"),

    
    #API CALLS ------------------------------------------------------------------   
    
    #return JSON ----------------------------------------------
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/search.json$',
         search_json, name="api_search_json_w_params"),
    
    #return CSV ------------------------------------------------
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/search.csv$',
         search_csv, name="api_search_csv_w_params"),
 
    #return HTML Table ----------------------------------------------------------  
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/search.html$',
         search_html, name="api_search_html_w_params"),
    
    #Saved Search API Calls ------------------------------------------------------- 
    url(r'^api/run-public-saved-search/(?P<slug>\S+)$',
        run_saved_search_by_slug,
        name="run_saved_search_by_slug"),
    
    url(r'^api/run-private-saved-search/(?P<slug>\S+)$',
        json_login_required(run_saved_search_by_slug),
        name="run_saved_search_by_slug"),
    
    #Complex Searches
    url(r'^api/complex-search$',
        json_login_required(csrf_exempt(complex_search)),
        name="api_complex_search"),
    
    url(r'^api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/complex-search$',
         json_login_required(csrf_exempt(complex_search)), name="api_complex_search"),

    )