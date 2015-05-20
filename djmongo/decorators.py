#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


"""
    Decorator to check for credentials before responding on API requests.
    REsponse with JSON instead of standard login redirect.
"""

import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs
from functools import update_wrapper, wraps
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from utils import authorize, unauthorized_json_response
from search.models import DatabaseAccessControl
import shlex
import json

def json_login_required(func):
    """
        Put this decorator before your view to check if the user is logged in
        and return a JSON 401 error if he/she is not.
    """
    
    def wrapper(request, *args, **kwargs):
        user= None
        #get the Basic username and password from the request.
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)
        
        if auth_string:
            (authmeth, auth) = auth_string.split(" ", 1)
            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)

        
            #print username, password  
            user = authenticate(username=username, password=password)
        
        if not user or not user.is_active:
            return HttpResponse(unauthorized_json_response(),
                    content_type="application/json")          
        login(request, user)
        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


def check_database_access(func):
    """
        Put this decorator before your view to check if the database/colelction
        can be accessed by this user, Return a JSON 401 error if he/she is not.
        Call after login decorator.
    """
    
    def wrapper(request, *args, **kwargs):
        default_to_open = getattr(settings, 'DEFAULT_TO_OPEN_READ', False)
        
        database_name   = kwargs.get('database_name', "")
        collection_name = kwargs.get('collection_name', "")
        
    
        if not default_to_open:
            
            if not database_name or not collection_name:
                return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")
            
            try:
                #Check to see if we have a matching record in DB access.
                dac = DatabaseAccessControl.objects.get(database_name=database_name,
                                                    collection_name=collection_name)      
            except DatabaseAccessControl.DoesNotExist:
                
                return HttpResponse(unauthorized_json_response(),
                                content_type="application/json")
            
            if not dac.is_public:
                dac_groups = dac.groups.all()
                user_groups = request.user.groups.all()
                
                print request.user, dac_groups, user_groups
                 #for g in dac.groups.all():
                    #if equest.user.groups.
                
               #allowedgroups
                in_group=False
                group= None
                for dg in  dac_groups:
                    if dg in user_groups:
                        in_group =True
                        group = dg
  
                if not in_group:
                    message = "NOT-IN-GROUP: You do not have access to this collection. Please see your system administrator."                  
                    
                    body={"code": 400,
                           "message": message,
                           "errors": [ message, ]}          
                    return HttpResponse(json.dumps(body, indent=4, ),
                                content_type="application/json")

                

            #If search keys have been limitied...
            if dac.search_keys:
                search_key_list = shlex.split(dac.search_keys)
                keys = []
                for k in request.GET.keys():
                    
                    if k not in search_key_list:
                        message = "Search key %s  is not allowed." % (k)                    
                    
                        body={"code": 400,
                           "message": k,
                           "errors": [ message, ]}
          
                        return HttpResponse(json.dumps(body, indent=4, ),
                                content_type="application/json")
        
        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)



