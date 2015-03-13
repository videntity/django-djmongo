#!/usr/bin/env python
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils import mongodb_ensure_index, create_mongo_db



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
    initial_document= forms.CharField(widget=forms.Textarea,
                                      initial = '{"foo":"bar"}')
    required_css_class = 'required'

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
    
    
class DocumentForm(forms.Form):
    document = forms.CharField(widget=forms.Textarea, initial='{"replace_me": true }')
    database_name = forms.CharField()
    collection_name = forms.CharField()
    
    required_css_class = 'required'