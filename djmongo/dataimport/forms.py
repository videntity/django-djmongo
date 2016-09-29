#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.forms import ModelForm
from .models import DataImport


class DataImportForm(ModelForm):

    class Meta:
        model = DataImport
        fields = ('file1', 'delete_collection_before_import',
                  'input_format', 'database_name', 'collection_name')
    required_css_class = 'required'
