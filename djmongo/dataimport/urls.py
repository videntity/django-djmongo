#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from ..decorators import httpauth_login_required
from django.conf.urls import url
from .views import (previous_data_imports, delete_import,
                    import_data_file)

urlpatterns = [
    url(r'^view$', login_required(previous_data_imports),
        name="djmongo_previous_data_imports"),

    url(r'^view/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(previous_data_imports),
        name="djmongo_previous_data_imports_w_params"),

    url(r'^delete/(?P<slug>\S+)$',
        login_required(delete_import),
        name="djmongo_delete_import_by_slug"),

    url(r'^csv$', login_required(import_data_file),
        name="djmongo_import_csv"),


    url(r'^csv/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        login_required(import_data_file),
        name="djmongo_import_csv_w_params"),

    # API calls ----------------------------------------------------------
    url(r'^api/csv$', httpauth_login_required(csrf_exempt(import_data_file)),
        name="djmongo_api_import_data_file"),

    url(r'^api/csv/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)$',
        httpauth_login_required(csrf_exempt(import_data_file)),
        name="djmongo_api_import_file_w_params"),

    url(r'^$',
        TemplateView.as_view(template_name='djmongo/console/import-home.html'),
        name="djmongo_import_home"),

]
