#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import WriteAPIHTTPAuth, WriteAPIIP, WriteAPIOAuth2
import json
from collections import OrderedDict


class WriteAPIHTTPAuthForm(forms.ModelForm):

    class Meta:
        model = WriteAPIHTTPAuth
        fields = (
            'slug',
            'http_post',
            'http_put',
            'database_name',
            'collection_name',
            'readme_md',
            'groups',
            'json_schema')
    required_css_class = 'required'

    def clean_json_schema(self):
        json_schema = self.cleaned_data["json_schema"]
        try:
            json.loads(json_schema, object_pairs_hook=OrderedDict)
        except ValueError:
            raise forms.ValidationError(_('The JSONSchema was invalid JSON'))
        return json_schema


class WriteAPIHTTPAuthDeleteForm(forms.Form):

    slug = forms.CharField(label=_("Slug"),
                           help_text=_("Retype the slug to confirm deletion."))

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        try:
            WriteAPIHTTPAuth.objects.get(slug=slug)
        except WriteAPIHTTPAuth.DoesNotExist:
            raise forms.ValidationError(_('There is no API with that slug.'))
        return slug


class WriteAPIIPForm(forms.ModelForm):

    class Meta:
        model = WriteAPIIP
        fields = (
            'slug',
            'http_post',
            'http_put',
            'database_name',
            'collection_name',
            'from_ip',
            'readme_md',
            'json_schema')
    required_css_class = 'required'

    def clean_json_schema(self):
        json_schema = self.cleaned_data["json_schema"]
        try:
            json_schema_load = json.loads(
                json_schema, object_pairs_hook=OrderedDict)
        except ValueError:
            raise forms.ValidationError(_('The JSONSchema was invalid JSON'))
        return json_schema


class WriteAPIIPDeleteForm(forms.Form):

    slug = forms.CharField(label=_("Slug"),
                           help_text=_("Retype the slug to confirm deletion."))

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        try:
            WriteAPIIP.objects.get(slug=slug)
        except WriteAPIIP.DoesNotExist:
            raise forms.ValidationError(_('There is no API with that slug.'))
        return slug


class WriteAPIOAuth2Form(forms.ModelForm):

    class Meta:
        model = WriteAPIOAuth2
        fields = (
            'slug',
            'http_post',
            'http_put',
            'database_name',
            'collection_name',
            'scopes',
            'readme_md',
            'json_schema')
    required_css_class = 'required'

    def clean_json_schema(self):
        json_schema = self.cleaned_data["json_schema"]
        try:
            json.loads(json_schema, object_pairs_hook=OrderedDict)
        except ValueError:
            raise forms.ValidationError(_('The JSON Schema was invalid JSON.'))
        return json_schema


class WriteAPIOAuth2DeleteForm(forms.Form):

    slug = forms.CharField(label=_("Slug"),
                           help_text=_("Retype the slug to confirm deletion."))

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        try:
            WriteAPIOAuth2.objects.get(slug=slug)
        except WriteAPIOAuth2.DoesNotExist:
            raise forms.ValidationError(_('There is no API with that slug.'))
        return slug
