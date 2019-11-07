#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib.auth.decorators import login_required
from ..decorators import httpauth_login_required
from ..decorators import (check_read_httpauth_access,
                          check_public_ok,
                          ipauth_read_verification_required,
                          custom_ipauth_read_verification_required)
from django.conf.urls import url
from .views.run import (run_public_delete_api,
                        run_httpauth_delete_api,
                        run_ipauth_delete_api)

from .views.ced import (create_delete_api, edit_delete_api, delete_delete_api)

urlpatterns = [

    # DELETE APIs ------------------------

    url(r'^api/public/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        check_public_ok(run_public_delete_api), name="djmongo_api_public_delete"),

    url(r'^api/httpauth/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        httpauth_login_required(check_read_httpauth_access(run_httpauth_delete_api)),
        name="djmongo_api_httpauth_delete"),

    url(r'^api/ipauth/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^.]+).(?P<output_type>[^/]+)$',
        ipauth_read_verification_required(run_ipauth_delete_api),
        name="djmongo_api_ipauth_delete"),

    # CRUD for Managing APIs

    # Create -------------------------------------
    url(r'^(?P<auth_type>[^/]+)/create-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(create_delete_api),
        name="djmongo_delete_api"),

    # Edit ----------------------------------------
    url(r'^(?P<auth_type>[^/]+)/edit-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(edit_delete_api),
        name="djmongo_edit_delete_api"),
    
    # Delete ----------------------------------------
    url(r'^(?P<auth_type>[^/]+)/delete-api/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<slug>[^/]+)$',
        login_required(delete_delete_api),
        name="djmongo_delete_delete_api"),


]
