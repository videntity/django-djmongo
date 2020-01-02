#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import write_to_collection_httpauth, write_to_collection_ip_auth
from .views import (create_oauth2_write_api, edit_oauth2_write_api,
                    delete_oauth2_write_api)
from .views import browse_ip_write_apis, browse_httpauth_write_apis
from .views import create_httpauth_write_api, create_ip_write_api
from .views import delete_httpauth_write_api, delete_ip_write_api
from .views import edit_httpauth_write_api, edit_ip_write_api

urlpatterns = [

    # Call / Run the write API
    url(r'^api/httpauth/(?P<slug>[^/]+)$',
        write_to_collection_httpauth,
        name="djmongo_api_write_to_collection_with_httpauth"),

    url(r'^api/ip/(?P<slug>[^/]+)$',
        write_to_collection_ip_auth,
        name="djmongo_api_write_to_collection_with_ip"),

    # Browse existing APIS in the UI
    url(r'^ip/browse-write-apis/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(browse_ip_write_apis),
        name="djmongo_browse_ip_write_apis_w_params"),

    url(r'^httpauth/browse-write-apis/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(browse_httpauth_write_apis),
        name="djmongo_browse_httpauth_write_apis_w_params"),

    url(r'^ip/browse-write-apis$',
        login_required(browse_ip_write_apis),
        name="djmongo_browse_ip_write_apis"),

    url(r'^httpauth/browse-write-apis$',
        login_required(browse_httpauth_write_apis),
        name="djmongo_browse_httpauth_write_apis"),
    # Create new APIs --------------------------------------------
    url(r'^httpauth/create-write-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_httpauth_write_api),
        name="djmongo_create_httpauth_write_api_w_params"),

    url(r'^oauth2/create-write-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_oauth2_write_api),
        name="djmongo_create_oauth2_write_api_w_params"),

    url(r'^ip/create-write-api$',
        login_required(create_ip_write_api),
        name="djmongo_create_ip_write_api"),

    url(r'^httpauth/create-write-api$',
        login_required(create_httpauth_write_api),
        name="djmongo_create_httpauth_write_api"),

    url(r'^ip/create-write-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_ip_write_api),
        name="djmongo_create_ip_write_api_w_params"),

    # Edit existing write APIs ---------------------
    url(r'^ip/edit-write-api/(?P<slug>[^/]+)$',
        login_required(edit_ip_write_api),
        name="djmongo_edit_ip_write_api"),

    url(r'^httpauth/edit-write-api/(?P<slug>[^/]+)$',
        login_required(edit_httpauth_write_api),
        name="djmongo_edit_httpauth_write_api"),

    url(r'^oauth2/edit-write-api/(?P<slug>[^/]+)$',
        login_required(edit_oauth2_write_api),
        name="djmongo_edit_oauth2_write_api"),

    # Delete existing write APIs ----------------------
    url(r'^ip/delete-write-api/(?P<slug>[^/]+)$',
        login_required(delete_ip_write_api),
        name="djmongo_delete_ip_write_api"),

    url(r'^httpauth/delete-write-api/(?P<slug>[^/]+)$',
        login_required(delete_httpauth_write_api),
        name="djmongo_delete_httpauth_write_api"),


    url(r'^oauth2/delete-write-api/(?P<slug>[^/]+)$',
        login_required(delete_oauth2_write_api),
        name="djmongo_delete_oauth2_write_api"),


]
