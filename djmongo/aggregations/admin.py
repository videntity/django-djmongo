#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin
from .models import Aggregation


class AggregationAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'user',
        'database_name',
        'collection_name',
        'output_collection_name',
        'creation_date')


admin.site.register(Aggregation, AggregationAdmin)
