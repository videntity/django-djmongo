#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from .models import (HTTPAuthDeleteAPI, PublicDeleteAPI,
                     IPAuthDeleteAPI, OAuth2DeleteAPI)


class OAuth2DeleteAPIForm(forms.ModelForm):

    class Meta:
        model = OAuth2DeleteAPI
        fields = ('slug', 'database_name', 'collection_name',
                  'search_keys', 'scopes', 'readme_md',)
    required_css_class = 'required'


class HTTPAuthDeleteAPIForm(forms.ModelForm):

    class Meta:
        model = HTTPAuthDeleteAPI
        fields = ('slug', 'database_name', 'collection_name',
                  'search_keys', 'groups', 'readme_md',)
    required_css_class = 'required'


class IPAuthDeleteAPIForm(forms.ModelForm):

    class Meta:
        model = IPAuthDeleteAPI
        fields = ('slug', 'database_name', 'collection_name',
                  'search_keys', 'from_ip', 'readme_md',)
    required_css_class = 'required'


class PublicDeleteAPIForm(forms.ModelForm):

    class Meta:
        model = PublicDeleteAPI
        fields = ('slug', 'database_name', 'collection_name',
                  'search_keys', 'readme_md',)
    required_css_class = 'required'
