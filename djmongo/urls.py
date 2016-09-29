#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^hello$', TemplateView.as_view(template_name='djmongo/console/splash.html'),
        name='djmongo_splash'),
    #url(r'^import/',   include('apps.djmongo.dataimport.urls')),
    url(r'^console/',  include('apps.djmongo.console.urls')),
    url(r'^search/',   include('apps.djmongo.search.urls')),
    url(r'^write/',    include('apps.djmongo.write.urls')),
    url(r'^accounts/', include('apps.djmongo.accounts.urls')),
    url(r'^aggregations/', include('apps.djmongo.aggregations.urls')),
]
 
                       
                       
