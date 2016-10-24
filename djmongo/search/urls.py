#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib.auth.decorators import login_required
from ..decorators import httpauth_login_required
from ..decorators import check_read_httpauth_access, check_public_ok
from django.conf.urls import url

from .views import run_custom_public_read_api_by_slug, run_custom_httpauth_read_api_by_slug

from .views import create_simple_api, create_custom_api

from .views import edit_custom_httpauth_read_api, edit_custom_public_read_api
from .views import edit_simple_httpauth_read_api, edit_simple_public_read_api

from .views import delete_custom_httpauth_read_api, delete_custom_public_read_api
from .views import delete_simple_httpauth_read_api, delete_simple_public_read_api

from .views import build_keys, simple_search


urlpatterns = [
    # Run Read APIs ------------------------

    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        check_public_ok(simple_search), name="djmongo_api_public_simple_search"),



    url(r'^api/httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        httpauth_login_required(check_read_httpauth_access(simple_search)),
        name="djmongo_api_httpauth_simple_search"),


    url(r'^api/custom/httpauth/(?P<slug>\S+)$',
        httpauth_login_required(run_custom_httpauth_read_api_by_slug),
        name="djmongo_run_custom_httpauth_read_api_by_slug"),

    url(r'^api/custom/public/(?P<slug>\S+)$',
        run_custom_public_read_api_by_slug,
        name="djmongo_run_custom_public_read_api_by_slug"),


    # CRUD for Managing APIs

    # Create -------------------------------------
    url(r'^simple/(?P<auth_type>[^/]+)/create-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_simple_api),
        name="djmongo_create_simple_api"),

    url(r'^custom/(?P<auth_type>[^/]+)/create-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_custom_api),
        name="djmongo_create_custom_api"),


    # Edit ----------------------------------------
    url(r'^simple/public/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(edit_simple_public_read_api),
        name="djmongo_edit_simple_public_read_api"),

    url(r'^simple/httpauth/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(edit_simple_httpauth_read_api),
        name="djmongo_edit_simple_httpauth_read_api"),

    url(r'^custom/httpauth/edit-api/(?P<slug>\S+)$',
        login_required(edit_custom_httpauth_read_api),
        name="djmongo_edit_custom_httpauth_read_api"),

    url(r'^custom/public/edit-api/(?P<slug>\S+)$',
        login_required(edit_custom_public_read_api),
        name="djmongo_edit_custom_public_read_api"),




    # Delete --------------------------------------
    url(r'^simple/public/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_simple_public_read_api),
        name="djmongo_delete_simple_public_read_api"),

    url(r'^simple/httpauth/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_simple_httpauth_read_api),
        name="djmongo_delete_simple_httpauth_read_api"),

    url(r'^custom/public/delete-api/(?P<slug>[^/]+)$',
        login_required(delete_custom_public_read_api),
        name="djmongo_delete_custom_public_read_api"),

    url(r'^custom/httpauth/delete-api/(?P<slug>[^/]+)$',
        login_required(delete_custom_httpauth_read_api),
        name="djmongo_delete_custom_httpauth_read_api"),



    # Build keys of a collection.
    url(r'^build-keys/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(build_keys),
        name="djmongo_build_keys"),


]
