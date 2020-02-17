#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls import url
from .views import simple_logout, simple_login

urlpatterns = [

    # Login.Logout of the web interface
    url(r'^logout$', simple_logout, name="djmongo_logout"),
    url(r'^login$', simple_login, name="djmongo_login"),
]
