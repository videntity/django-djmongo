#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from .models import SavedSearch, DatabaseAccessControl, PublicReadAPI
from django.utils.translation import ugettext_lazy as _


class DatabaseAccessControlForm(forms.ModelForm):

    class Meta:
        model = DatabaseAccessControl
        fields = ('database_name', 'collection_name',
                  'is_public', 'search_keys', 'groups')
    required_css_class = 'required'

class PublicReadAPIForm(forms.ModelForm):

    class Meta:
        model = PublicReadAPI
        fields = ('database_name', 'collection_name',
                  'search_keys',)
    required_css_class = 'required'


PublicReadAPI

class SavedSearchForm(forms.ModelForm):

    class Meta:
        model = SavedSearch
        fields = ('slug', 'query', 'group', 'is_public', 'type_mapper',
                  'return_keys', 'sort', 'default_limit',
                  'database_name', 'collection_name', 'output_format')

    required_css_class = 'required'
