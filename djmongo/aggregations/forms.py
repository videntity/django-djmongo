#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json
from django import forms
from .models import Aggregation
from django.utils.translation import ugettext_lazy as _


class AggregationForm(forms.ModelForm):
    class Meta:
        model = Aggregation
        fields = ( 'slug', 'pipeline',
                  'database_name', 'collection_name',
                  'output_collection_name','execute_time_1', 'description')

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
    
