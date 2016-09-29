#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.contrib import admin
from .models import CreateHistory


class CreateHistoryAdmin(admin.ModelAdmin):
    list_display = ('database_name', 'collection_name', 'history')
admin.site.register(CreateHistory, CreateHistoryAdmin)
