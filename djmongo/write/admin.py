#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin
from .models import WriteAPIHTTPAuth, WriteAPIIP, WriteAPIoAuth2


class WriteAPIHTTPAuthAdmin(admin.ModelAdmin):
    list_display = ('slug', 'database_name',
                    'collection_name', 'creation_date')


admin.site.register(WriteAPIHTTPAuth, WriteAPIHTTPAuthAdmin)


class WriteAPIIPAdmin(admin.ModelAdmin):
    list_display = ('slug', 'database_name',
                    'collection_name', 'from_ip', 'creation_date')


admin.site.register(WriteAPIIP, WriteAPIIPAdmin)


class WriteAPIoAuth2Admin(admin.ModelAdmin):
    list_display = ('slug', 'database_name',
                    'collection_name', 'creation_date')


admin.site.register(WriteAPIoAuth2, WriteAPIoAuth2Admin)
