#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime
from django import forms
from models import SavedSearch, OUTPUT_CHOICES
from django.utils.translation import ugettext_lazy as _



class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ('title', 'query','return_keys', 'sort', 'default_limit',
                  'database_name', 'collection_name', 'output_format')

    required_css_class = 'required'
    
    
class ComplexSearchForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, initial="{}")
    skip = forms.IntegerField(initial=0)
    limit = forms.IntegerField(initial=200)
    sort = forms.CharField(widget=forms.Textarea, initial="", required=False,
             help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")
    database_name = forms.CharField()
    collection_name = forms.CharField()
    output_format = forms.TypedChoiceField(choices=OUTPUT_CHOICES,
                                           initial="json")
    required_css_class = 'required'
    
