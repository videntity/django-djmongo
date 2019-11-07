#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from ..decorators import httpauth_login_required
from ..decorators import (check_read_httpauth_access,
                          check_public_ok,
                          ipauth_read_verification_required,
                          custom_ipauth_read_verification_required)

from .views.run import (build_keys, simple_search, run_custom_public_read_api_by_slug,
                        run_custom_httpauth_read_api_by_slug,
                        run_custom_ipauth_read_api_by_slug)

from .views.ced import create_simple_api, create_custom_api
from .views.ced import (edit_custom_httpauth_read_api, edit_custom_public_read_api,
                        edit_custom_ipauth_read_api, edit_custom_oauth2_read_api)

from .views.ced import (edit_simple_httpauth_read_api, edit_simple_public_read_api,
                        edit_simple_ipauth_read_api, edit_simple_oauth2_read_api)

from .views.ced import (delete_custom_httpauth_read_api, delete_custom_public_read_api,
                        delete_custom_ipauth_read_api, delete_custom_oauth2_read_api)
from .views.ced import (delete_simple_httpauth_read_api, delete_simple_public_read_api,
                        delete_simple_oauth2_read_api, delete_simple_ipauth_read_api)

urlpatterns = [
    # Run Read APIs ------------------------

    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        check_public_ok(simple_search), name="djmongo_api_public_simple_search"),

    url(r'^api/httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        httpauth_login_required(check_read_httpauth_access(simple_search)),
        name="djmongo_api_httpauth_simple_search"),

    url(r'^api/ipauth/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        ipauth_read_verification_required(simple_search),
        name="djmongo_api_ipauth_simple_search"),


    url(r'^api/custom/httpauth/(?P<slug>\S+)$',
        httpauth_login_required(run_custom_httpauth_read_api_by_slug),
        name="djmongo_run_custom_httpauth_read_api_by_slug"),

    url(r'^api/custom/public/(?P<slug>\S+)$',
        run_custom_public_read_api_by_slug,
        name="djmongo_run_custom_public_read_api_by_slug"),

    url(r'^api/custom/ipauth/(?P<slug>\S+)$',
        custom_ipauth_read_verification_required(
            run_custom_ipauth_read_api_by_slug),
        name="djmongo_run_custom_ipauth_read_api_by_slug"),

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

    url(r'^simple/oauth2/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(edit_simple_oauth2_read_api),
        name="djmongo_edit_simple_oauth2_read_api"),

    url(r'^simple/ipauth/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(edit_simple_ipauth_read_api),
        name="djmongo_edit_simple_ipauth_read_api"),


    url(r'^custom/httpauth/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>\S+)$',
        login_required(edit_custom_httpauth_read_api),
        name="djmongo_edit_custom_httpauth_read_api"),

    url(r'^custom/public/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>\S+)$',
        login_required(edit_custom_public_read_api),
        name="djmongo_edit_custom_public_read_api"),

    url(r'^custom/oauth2/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>\S+)$',
        login_required(edit_custom_oauth2_read_api),
        name="djmongo_edit_custom_oauth2_read_api"),

    url(r'^custom/ipauth/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>\S+)$',
        login_required(edit_custom_ipauth_read_api),
        name="djmongo_edit_custom_ipauth_read_api"),




    # Delete --------------------------------------
    url(r'^simple/public/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_simple_public_read_api),
        name="djmongo_delete_simple_public_read_api"),

    url(r'^simple/httpauth/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_simple_httpauth_read_api),
        name="djmongo_delete_simple_httpauth_read_api"),

    url(r'^simple/oauth2/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_simple_oauth2_read_api),
        name="djmongo_delete_simple_oauth2_read_api"),

    url(r'^simple/ipauth/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_simple_ipauth_read_api),
        name="djmongo_delete_simple_ipauth_read_api"),


    url(r'^custom/public/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_custom_public_read_api),
        name="djmongo_delete_custom_public_read_api"),

    url(r'^custom/httpauth/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_custom_httpauth_read_api),
        name="djmongo_delete_custom_httpauth_read_api"),

    url(r'^custom/oauth2/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_custom_oauth2_read_api),
        name="djmongo_delete_custom_oauth2_read_api"),

    url(r'^custom/ipauth/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_custom_ipauth_read_api),
        name="djmongo_delete_custom_ipauth_read_api"),


    # Build keys of a collection.
    url(r'^build-keys/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(build_keys),
        name="djmongo_build_keys"),


]
