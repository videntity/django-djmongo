#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [

    url(r'^import/', include('djmongo.dataimport.urls')),
    url(r'^console/', include('djmongo.console.urls')),
    url(r'^read/', include('djmongo.read.urls')),
    url(r'^read/', include('djmongo.read.oauth2_urls')),
    url(r'^write/', include('djmongo.write.urls')),
    url(r'^write/', include('djmongo.write.oauth2_urls')),
    url(r'^delete/', include('djmongo.delete.urls')),
    url(r'^accounts/', include('djmongo.accounts.urls')),
    url(r'^aggregations/', include('djmongo.aggregations.urls')),
    url(r'^$', TemplateView.as_view(template_name='djmongo/console/splash.html'),
        name='djmongo_splash'),
    # Django OAuth Toolkit
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
