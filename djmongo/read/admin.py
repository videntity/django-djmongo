#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin
from .models import (PublicReadAPI, HTTPAuthReadAPI,
                     OAuth2ReadAPI, IPAuthReadAPI,
                     CustomHTTPAuthReadAPI, CustomPublicReadAPI,
                     CustomIPAuthReadAPI, CustomOAuth2ReadAPI)


class CustomOAuth2ReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'url')


admin.site.register(CustomOAuth2ReadAPI, CustomOAuth2ReadAPIAdmin)


class CustomHTTPAuthReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'url')


admin.site.register(CustomHTTPAuthReadAPI, CustomHTTPAuthReadAPIAdmin)


class CustomIPAuthReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'url')


admin.site.register(CustomIPAuthReadAPI, CustomIPAuthReadAPIAdmin)


class CustomPublicReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name',
                    'url')


admin.site.register(CustomPublicReadAPI, CustomPublicReadAPIAdmin)


class HTTPAuthReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'json_url')


admin.site.register(HTTPAuthReadAPI, HTTPAuthReadAPIAdmin)


class IPAuthReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'json_url')


admin.site.register(IPAuthReadAPI, IPAuthReadAPIAdmin)


class PublicReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'json_url',)


admin.site.register(PublicReadAPI, PublicReadAPIAdmin)


class OAuth2ReadAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'json_url',)


admin.site.register(OAuth2ReadAPI, OAuth2ReadAPIAdmin)
