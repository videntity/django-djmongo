#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin
from .models import (HTTPAuthDeleteAPI, IPAuthDeleteAPI,
                     OAuth2DeleteAPI, PublicDeleteAPI)


class HTTPAuthDeleteAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'url')


admin.site.register(HTTPAuthDeleteAPI, HTTPAuthDeleteAPIAdmin)


class IPAuthDeleteAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'url')


admin.site.register(IPAuthDeleteAPI, IPAuthDeleteAPIAdmin)


class PublicDeleteAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'url',)


admin.site.register(PublicDeleteAPI, PublicDeleteAPIAdmin)


class OAuth2DeleteAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'url',)


admin.site.register(OAuth2DeleteAPI, OAuth2DeleteAPIAdmin)
