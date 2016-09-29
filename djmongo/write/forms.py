#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import WriteAPIHTTPAuth, WriteAPIIP


class WriteAPIHTTPAuthForm(forms.ModelForm):

    class Meta:
        model = WriteAPIHTTPAuth
        fields = (
            'slug',
            'database_name',
            'collection_name',
            'groups',
            'json_schema')
    required_css_class = 'required'


class WriteAPIHTTPAuthDeleteForm(forms.Form):

    slug = forms.CharField(label=_("Slug"),
                           help_text=_("Retype the slug to confirm deletion."))

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        try:
            WriteAPIHTTPAuth.objects.get(slug=slug)
        except WriteAPIHTTPAuth.DoesNotExist:
            raise forms.ValidationError(_('There is no API with that slug.'))


class WriteAPIIPForm(forms.ModelForm):

    class Meta:
        model = WriteAPIIP
        fields = (
            'slug',
            'database_name',
            'collection_name',
            'from_ip',
            'json_schema')
    required_css_class = 'required'


class WriteAPIIPDeleteForm(forms.Form):

    slug = forms.CharField(label=_("Slug"),
                           help_text=_("Retype the slug to confirm deletion."))

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        try:
            WriteAPIIP.objects.get(slug=slug)
        except WriteAPIIP.DoesNotExist:
            raise forms.ValidationError(_('There is no API with that slug.'))
