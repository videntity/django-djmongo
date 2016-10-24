#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..decorators import httpauth_login_required
from django.conf.urls import url
from .views import (showdbs, create_new_database,
                    create_collection, drop_collection,
                    simple_ensure_index, create_document_in_collection,
                    update_document_in_collection, drop_database,
                    show_apis)

urlpatterns = [

    url(r'^$', login_required(showdbs), name="djmongo_show_dbs"),

    url(r'^show-apis/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)',
        login_required(show_apis), name="djmongo_show_apis"),

    url(r'^new-database$', create_new_database,
        name="djmongo_create_new_database"),

    url(r'^drop-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)',
        login_required(drop_collection), name="djmongo_drop_collection"),

    url(r'^ensure-index/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(simple_ensure_index), name="djmongo_ensure_index"),

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

    # API calls --------------------------------------------------------------

    url(r'^api/drop-collection/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        httpauth_login_required(drop_collection),
        name="djmongo_api_delete_collection"),

    url(r'^api/ensure-index/(?P<database_name>[^/]+)/(?P<collection_name>\[^/]+)$',
        httpauth_login_required(csrf_exempt(simple_ensure_index)),
        name="djmongo_api_djmongo_ensure_indexe"),

    url(r'^api/drop-database/(?P<database_name>[^/]+)$',
        httpauth_login_required(drop_database),
        name="djmongo_api_drop_database"),

    url(r'^api/create-collection/(?P<database_name>[^/]+)$',
        httpauth_login_required(create_collection),
        name="djmongo_api_create_collection"),

]
