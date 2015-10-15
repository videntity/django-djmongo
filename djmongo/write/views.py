#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import os, uuid, json, sys
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..decorators import json_login_required, ip_verification_required, kickout_400, kickout_404, kickout_500, kickout_401
from django.http import HttpResponse
from collections import OrderedDict
from ..mongoutils import write_mongo
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from models import WriteAPIHTTPAuth, WriteAPIIP
# Create your views here.


@csrf_exempt
@json_login_required
def write_to_collection_httpauth(request, slug):
    errors = []
    
    try:
        wapi = WriteAPIHTTPAuth.objects.get(slug=slug)
    except WriteAPIHTTPAuth.DoesNotExist:
        return kickout_404("The API was not not found. Perhaps you need to define it?")
    
    
    if request.method == 'GET': #----------------------------------------------------
        try:
            json_schema = json.loads(wapi.json_schema, object_pairs_hook=OrderedDict)
            return HttpResponse(json.dumps(json_schema, indent=4), content_type="application/json")  
        except:
            return kickout_500("The JSON Schema did not contain valid JSON")
            
    
    if request.method == 'POST': #----------------------------------------------------
        
        #Check if request body is JSON ------------------------
        try:
            j =json.loads(request.body, object_pairs_hook=OrderedDict)
            if type(j) !=  type({}):
                kickout_400("The request body did not contain a JSON object i.e. {}.")
        except:
            return kickout_400("The request body did not contain valid JSON.")
        
        #check json_schema is valid
        try:
            json_schema = json.loads(wapi.json_schema, object_pairs_hook=OrderedDict)
              
        except:
            return kickout_500("The JSON Schema on the server did not contain valid JSON")
        
        #Check jsonschema
        if json_schema:
            try: 
                validate(j, json_schema)
            except ValidationError:
                msg = "JSON Schema Conformance Error. %s" % (str(sys.exc_info()[1][0]))
                return kickout_400(msg)
                 
        
        #write_to_mongo
        response = write_mongo(j, wapi.database_name, wapi.collection_name)
        return HttpResponse(json.dumps(response, indent=4),
                                    content_type="application/json") 


@csrf_exempt
@ip_verification_required
def write_to_collection_ip_auth(request, slug):
    errors = []
    try:
        wapi = WriteAPIIP.objects.get(slug=slug)
    except WriteAPIIP.DoesNotExist:
        return kickout_404("The API was not not found. Perhaps you need to define it?")
    
    if request.method == 'GET': #----------------------------------------------------
        try:
            json_schema = json.loads(wapi.json_schema, object_pairs_hook=OrderedDict)
            return HttpResponse(json.dumps(json_schema, indent=4), content_type="application/json")  
        except:
            return kickout_500("The JSON Schema did not contain valid JSON")
            
    
    if request.method == 'POST': #----------------------------------------------------
        
        #Check if request body is JSON ------------------------
        try:
            j =json.loads(request.body, object_pairs_hook=OrderedDict)
            if type(j) !=  type({}):
                kickout_400("The request body did not contain a JSON object i.e. {}.")
        except:
            return kickout_400("The request body did not contain valid JSON.")
        
        #check json_schema is valid
        try:
            json_schema = json.loads(wapi.json_schema, object_pairs_hook=OrderedDict)
              
        except:
            return kickout_500("The JSON Schema on the server did not contain valid JSON")
        
        #Check jsonschema
        if json_schema:
            try: 
                validate(j, json_schema)
            except ValidationError:
                msg = "JSON Schema Conformance Error. %s" % (str(sys.exc_info()[1][0]))
                return kickout_400(msg)
                 
        
        #write_to_mongo
        response = write_mongo(j, wapi.database_name, wapi.collection_name)
        return HttpResponse(json.dumps(response, indent=4),
                                    content_type="application/json") 

            
    