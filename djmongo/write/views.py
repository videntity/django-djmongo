#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import os, uuid, json, sys
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..decorators import check_database_access
from django.shortcuts import render,  get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from models import WriteAPI
from collections import OrderedDict
from ..mongoutils import write_mongo
from jsonschema import validate
from jsonschema.exceptions import ValidationError
# Create your views here.

@csrf_exempt
def write_to_collection(request, slug):
    errors = []
    wapi = get_object_or_404(WriteAPI, slug=slug)
    
    if request.method == 'GET': #----------------------------------------------------
        try:
            json_schema = json.loads(wapi.json_schema, object_pairs_hook=OrderedDict)
            return HttpResponse(json.dumps(json_schema, indent=4), content_type="application/json")  
        except:
            return kickout("The JSON Schema did not contain valid JSON")
            
    
    if request.method == 'POST': #----------------------------------------------------
        
        #Check if request body is JSON ------------------------
        try:
            j =json.loads(request.body, object_pairs_hook=OrderedDict)
            if type(j) !=  type({}):
                kickout("The string did not contain a JSON object.")
        except:
            return kickout("The request body did not contain valid JSON.")
        
        #check json_schema is valid
        try:
            json_schema = json.loads(wapi.json_schema, object_pairs_hook=OrderedDict)
              
        except:
            return kickout("The JSON Schema did not contain valid JSON")
        
        #Check jsonschema
        if json_schema:
            try: 
                validate(j, json_schema)
            except ValidationError:
                msg = "JSON Schema Conformance Error. %s" % (str(sys.exc_info()[1][0]))
                return kickout(msg)
                 
        
        #write_to_mongo
        response = write_mongo(j, wapi.database_name, wapi.collection_name)
        return HttpResponse(json.dumps(response, indent =4),
                                    content_type="application/json") 

def kickout(reason):
    response= OrderedDict()
    response["code"] = 400
    response["status"] = "Error"
    response["message"] = reason
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent =4), content_type="application/json") 
            
    