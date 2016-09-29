#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib.auth.decorators import login_required
from ..decorators import json_login_required
from ..decorators import check_read_httpauth_access, check_public_ok
from django.conf.urls import url
from .views import run_saved_search_by_slug, edit_saved_search_by_slug, delete_saved_search_by_slug
from .views import create_saved_search, browse_saved_searches, build_keys, setup_get_httpauth
from .views import search_csv, search_json, search_html, setup_get_public

urlpatterns = [
    # Run Saved Search
    url(r'^saved-search/(?P<slug>\S+)$',
        login_required(run_saved_search_by_slug),
        name="djmongo_run_saved_search_by_slug"),

    url(r'^public/saved-search/(?P<slug>\S+)$',
        run_saved_search_by_slug,
        name="djmongo_run_public_saved_search_by_slug"),
    
    # Edit Saved Search
    url(r'^edit-saved-search/(?P<slug>\S+)$',
        login_required(edit_saved_search_by_slug),
        name="djmongo_edit_saved_search_by_slug"),
    
    # Delete saved search
    url(r'^delete-saved-search/(?P<slug>\S+)$',
        login_required(delete_saved_search_by_slug),
        name="djmongo_delete_saved_search_by_slug"),
    
    # create saved search
    url(r'^create-saved-search/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_saved_search),
        name="djmongo_create_saved_search_w_params"),

    # Setup HTTP GET Httpauth
    url(r'^setup-get-public/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(setup_get_public),
        name="djmongo_setup_get_public"),

    # Setup HTTP GET Httpauth
    url(r'^setup-get-httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(setup_get_httpauth),
        name="djmongo_setup_get_httpauth"),


    # Browse saved searches
    url(r'^browse-saved-searches/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(browse_saved_searches),
        name="djmongo_browse_saved_searches_w_params"),

    # Unsupported/Experimental
    url(r'^build-keys/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(build_keys),
        name="djmongo_build_keys"),


    # Search API CALLS ------------------------------------------------------
    # Public URLs 
    # return JSON 
    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
        check_public_ok(search_json), name="djmongo_api_public_search_json_w_params"),

    # return CSV -
    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
        check_public_ok(search_csv), name="djmongo_api_public_search_csv_w_params"),

    # return HTML Table 
    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
        check_public_ok(search_html), name="djmongo_api_public_search_html_w_params"),
   
    #HTTP Auth URLs 
    # return JSON
    url(r'^api/httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).json$',
        json_login_required(check_read_httpauth_access(search_json)),
        name="djmongo_api_httpauth_search_json_w_params"),

    # return CSV 
    url(r'^api/httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).csv$',
        json_login_required(check_read_httpauth_access(search_csv)),
        name="djmongo_api_httpauth_search_csv_w_params"),

    # return HTML Table 
    url(r'^api/httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^.]+).html$',
        json_login_required(check_read_httpauth_access(search_html)),
        name="djmongo_api_httpauth_search_html_w_params"),


    # Saved Search API Calls -------------------------------------------------
    url(r'^api/public/saved-search/(?P<slug>\S+)$',
        run_saved_search_by_slug,
        name="djmongo_api_run_public_saved_search_by_slug"),

    url(r'^api/saved-search/(?P<slug>\S+)$',
        json_login_required(run_saved_search_by_slug),
        name="djmongo_api_run_saved_search_by_slug"),

]
