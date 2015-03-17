#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from  django.views.generic.base import TemplateView


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='djmongo/console/splash.html'),
        name="djmongo_splash"),
    
    
    )
