#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from .models import (HTTPAuthReadAPI, PublicReadAPI,
                     CustomHTTPAuthReadAPI, CustomPublicReadAPI)


class HTTPAuthReadAPIForm(forms.ModelForm):

    class Meta:
        model = HTTPAuthReadAPI
        fields = ('slug', 'database_name', 'collection_name',
                  'search_keys', 'groups')
    required_css_class = 'required'


class PublicReadAPIForm(forms.ModelForm):

    class Meta:
        model = PublicReadAPI
        fields = ('slug', 'database_name', 'collection_name',
                  'search_keys',)
    required_css_class = 'required'


class CustomHTTPAuthReadAPIForm(forms.ModelForm):

    class Meta:
        model = CustomHTTPAuthReadAPI
        fields = ('slug', 'query', 'group', 'type_mapper',
                  'return_keys', 'sort', 'default_limit',
                  'database_name', 'collection_name', 'output_format')

    required_css_class = 'required'


class CustomPublicReadAPIForm(forms.ModelForm):

    class Meta:
        model = CustomPublicReadAPI
        fields = ('slug', 'query', 'type_mapper',
                  'return_keys', 'sort', 'default_limit',
                  'database_name', 'collection_name', 'output_format')

    required_css_class = 'required'
