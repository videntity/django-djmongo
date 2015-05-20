#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime
from django import forms
from models import SavedSearch, OUTPUT_CHOICES, Aggregation
from django.utils.translation import ugettext_lazy as _
import json



class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ('group', 'title', 'query', 'type_mapper','return_keys', 'is_public', 'sort', 'default_limit',
                  'database_name', 'collection_name', 'output_format')

    required_css_class = 'required'
    


class AggregationForm(forms.ModelForm):
    class Meta:
        model = Aggregation
        fields = ( 'slug', 'pipeline',
                  'database_name', 'collection_name',
                  'output_collection_name','execute_now', 'description')

    required_css_class = 'required'
    def clean_pipeline(self):
        pipeline = self.cleaned_data.get('pipeline')

        try:
            j = json.loads(pipeline)
            if type (j) != type([]):
                msg="pipeline is not an array/list."
                raise forms.ValidationError(msg)
            else:
                for i in j:
                    if type(i)!=type({}):
                        msg="pipeline is not an array/list of dicts."
                        raise forms.ValidationError(msg)
                    if i.has_key("$out"):
                       msg="Do not provide $out in your pipeline. Use output_collection_name instead."
                       raise forms.ValidationError(msg) 
                
        
        except ValueError:  
            msg="pipeline field does not contain valid JSON."
            raise forms.ValidationError(msg)
        
        return pipeline
    

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
    
