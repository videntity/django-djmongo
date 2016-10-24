#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin
from .models import (PublicReadAPI, HTTPAuthReadAPI,
                     CustomHTTPAuthReadAPI, CustomPublicReadAPI)


class CustomHTTPAuthReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'creation_date')
admin.site.register(CustomHTTPAuthReadAPI, CustomHTTPAuthReadAPIAdmin)


class CustomPublicReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'creation_date')
admin.site.register(CustomPublicReadAPI, CustomPublicReadAPIAdmin)


class HTTPAuthReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name')
admin.site.register(HTTPAuthReadAPI, HTTPAuthReadAPIAdmin)


class PublicReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name')
admin.site.register(PublicReadAPI, PublicReadAPIAdmin)
