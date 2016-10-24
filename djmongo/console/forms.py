#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django import forms
from django.utils.translation import ugettext_lazy as _
from .utils import mongodb_ensure_index, create_mongo_db
import json


class ConfirmDropForm(forms.Form):
    name = forms.CharField(max_length=256)
    required_css_class = 'required'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label=_("User"))
    password = forms.CharField(widget=forms.PasswordInput, max_length=30,
                               label=_("Password"))
    required_css_class = 'required'


class EnsureIndexForm(forms.Form):
    key = forms.CharField(label=_("Key"))
    database_name = forms.CharField()
    collection_name = forms.CharField()
    required_css_class = 'required'

    def save(self, database_name, collection_name):
        key = self.cleaned_data["key"]
        result = mongodb_ensure_index(database_name, collection_name, key)
        return result


class CreateDatabaseForm(forms.Form):

    database_name = forms.CharField()
    collection_name = forms.CharField()
    initial_document = forms.CharField(
        widget=forms.Textarea,
        help_text="""You must create a document in order to
                     create a new database and collection""")
    required_css_class = 'required'

    def clean_initial_document(self):

        initial_document = self.cleaned_data.get('initial_document', '')

        try:
            djson = json.loads(initial_document)
            if not isinstance(djson, type({})):
                raise forms.ValidationError('Not a JSON object (i.e. {} )')

        except ValueError:
            raise forms.ValidationError('Invalid JSON.')

        return initial_document

    def save(self):

        result = create_mongo_db(self.cleaned_data["database_name"],
                                 self.cleaned_data["collection_name"],
                                 self.cleaned_data["initial_document"])
        return result


class DeleteForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, initial="{}")
    just_one = forms.BooleanField(required=False)
    database_name = forms.CharField()
    collection_name = forms.CharField()

    required_css_class = 'required'

    def clean_query(self):

        query = self.cleaned_data.get('query', '')

        try:
            djson = json.loads(query)
            if not isinstance(djson, type({})):
                raise forms.ValidationError("""Not a JSON
                                            object (i.e. {} )""")

        except ValueError:
            raise forms.ValidationError('Invalid JSON.')

        return query


class DocumentForm(forms.Form):
    document = forms.CharField(widget=forms.Textarea)
    database_name = forms.CharField()
    collection_name = forms.CharField()

    required_css_class = 'required'

    def clean_document(self):

        document = self.cleaned_data.get('document', '')

        try:
            djson = json.loads(document)
            if not isinstance(djson, type({})):
                raise forms.ValidationError('Not a JSON object (i.e. {} )')

        except ValueError:
            raise forms.ValidationError('Invalid JSON.')

        return document
