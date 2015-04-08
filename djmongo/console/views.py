#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import json
from django.conf import settings
from django.shortcuts import render_to_response, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from utils import (show_dbs, mongodb_drop_collection, mongodb_drop_database,
                mongodb_clear_collection, mongodb_ensure_index)

from forms import EnsureIndexForm, DeleteForm, DocumentForm, CreateDatabaseForm, LoginForm
from utils import mongo_delete_json_util, mongo_create_json_util
from bson.objectid import ObjectId
from django.contrib.auth import authenticate, login, logout

def showdbs(request):
    dbs = show_dbs()
    if not dbs:
        messages.error(request, "No databases were found. You haven't created any yet, MongoDB isn't running, or its not connected.")
    context = { "dbs": dbs }
    return render_to_response('djmongo/console/showdbs.html',
                              RequestContext(request, context,))



def simple_logout(request):
    logout(request)
    messages.success(request, _("Logged out successfully."))
    return HttpResponseRedirect(reverse('djmongo_login'))


def simple_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    
                    next = request.GET.get('next','')
                    if next:
                        #If a next is in the URL, then go there
                        return HttpResponseRedirect(next)
                    #otherwise just go to home.
                    return HttpResponseRedirect(reverse('djmongo_show_dbs'))
                else:
                   #The user exists but is_active=False
                   messages.error(request,
                        _("Your account is inactive so you may not log in."))
                   
                   return render_to_response('djmongo/console/login2.html',
                                            {'form': form},
                                            RequestContext(request))
            else:
                messages.error(request, _("Invalid username or password."))
                   
                return render_to_response('djmongo/console/login2.html',
                                    {'form': form},
                                    RequestContext(request))

        else:
         return render_to_response('djmongo/console/login2.html',
                              RequestContext(request, {'form': form}))
    #this is a GET
    return render_to_response('djmongo/console/login2.html',
                              {'form': LoginForm()},
                              context_instance = RequestContext(request))



def drop_collection(request, database_name, collection_name):
    response = mongodb_drop_collection(database_name, collection_name)
    #print response
    if response:
        errormsg = _("ERROR", response)
        messages.error(request,errormsg)
        
        return HttpResponseRedirect(reverse('djmongo_show_dbs'))
    else:
        messages.success(request,_("The collection was deleted."))
        return HttpResponseRedirect(reverse('djmongo_show_dbs'))



def drop_database(request, database_name):
    """Drop a MongoDB database"""
    
    response = mongodb_drop_database(database_name)
    #print response
    if response:
        errormsg = _("ERROR", response)
        messages.error(request,errormsg)
        return HttpResponseRedirect(reverse('djmongo_show_dbs'))
    else:
        messages.success(request,_("The database was deleted."))
        return HttpResponseRedirect(reverse('djmongo_show_dbs'))



def clear_collection(request, database_name, collection_name):
    """Clear a MongoDB database collection"""
    response = mongodb_clear_collection(database_name, collection_name)
    print response
    
    if response:
        errormsg = _("ERROR", response)
        messages.error(request,errormsg)
        
        return HttpResponseRedirect(reverse('djmongo_show_dbs'))
    else:
        messages.success(request,_("All records were removed from the collection."))
        return HttpResponseRedirect(reverse('djmongo_show_dbs'))



def simple_ensure_index(request,  database_name, collection_name):
    """Ensure a MongoDB index on a particular field name"""
    name = "Ensure a MongoDB index on a particular field name"

    if request.method == 'POST':
        form = EnsureIndexForm(request.POST)

        if form.is_valid():
            result = form.save(database_name, collection_name)        
            messages.success(request,_("Index created successfully"))
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            #The form is invalid
            messages.error(request,_("Please correct the errors in the form."))
            return render_to_response('djmongo/console/generic/bootstrapform.html',
                                           {'form': form,
                                            'name':name,
                                            },
                                           RequestContext(request))
        
    else:
        #this is a GET

        context= {'name':name,
                'form': EnsureIndexForm(
                            initial = {"database_name":   database_name,
                                       "collection_name": collection_name})
        }              
        return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))



def create_new_database(request):
    """Create a New Mongo Database by adding a single document."""
    name = "Create a New MongoDB Database"

    if request.method == 'POST':
        form = CreateDatabaseForm(request.POST)

        if form.is_valid():
            result = form.save()
            if result.has_key("error"):
                messages.error(request,"The database creation operation failed.")
                messages.error(request,result["error"])
            else:
                messages.success(request,"Database created.")
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            #The form is invalid
            messages.error(request,_("Please correct the errors in the form."))
            return render_to_response('djmongo/console/generic/bootstrapform.html',
                                           {'form': form,
                                            'name':name,
                                            },
                                           RequestContext(request))
        
    else:
        #this is a GET

        context= {'name':name,
                'form': CreateDatabaseForm(
                            initial = {"initial_document": '{ "foo" : "bar" }'
                                       })
        }              
        return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))



def create_collection(request, database_name):
    """Create a new mongo collection by adding a single document."""
    name = "Create a new collection"

    if request.method == 'POST':
        form = CreateDatabaseForm(request.POST)

        if form.is_valid():
            result = form.save()
            if result.has_key("error"):
                messages.error(request,"The database creation operation failed.")
                messages.error(request,result["error"])
            else:
                messages.success(request,"Collection created.")
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            #The form is invalid
            messages.error(request,_("Please correct the errors in the form."))
            return render_to_response('djmongo/console/generic/bootstrapform.html',
                                           {'form': form,
                                            'name':name,
                                            },
                                           RequestContext(request))
        
    else:
        #this is a GET

        context= {'name':name,
                'form': CreateDatabaseForm(
                            initial = {"initial_document": '{ "foo" : "bar" }',
                                       "database_name": database_name})
        }              
        return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))



def remove_data_from_collection(request,  database_name, collection_name):
    
    name = _("Delete select information from a MongoDB Collection based on a query")
    
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            just_one = form.cleaned_data['just_one']

            #run the delete
            results = mongo_delete_json_util(query, database_name=database_name,
                                             collection_name=collection_name,
                                             just_one=just_one)
            
            #convert to json and respond.
            results_json = json.dumps(results, indent =4)
            return HttpResponse(results_json, status=int(results['code']),
                                    content_type="application/json")        
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('djmongo/console/generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
    
    #this is a GET
    idata ={'database_name': database_name,
             'collection_name': collection_name,
             }
    

    context= {'name':name,
              'form': DeleteForm(initial=idata)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))



def create_document_in_collection(request, database_name,collection_name):

    name = _("Create a Document from JSON")
    
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data['document']
        
            #create the document
            results = mongo_create_json_util(document, database_name=database_name,
                                             collection_name=collection_name)
            
            #convert to json and respond.
            results_json = json.dumps(results, indent = 4)
            return HttpResponse(results_json, status=int(results['code']),
                                    content_type="application/json")        
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('djmongo/console/generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
    #this is a GET
    idata ={'database_name': database_name,
             'collection_name': collection_name,
             }
    
    context= {'name':name,
              'form': DocumentForm(initial=idata)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))
    

    
def update_document_in_collection(request,  database_name, collection_name):
    name = _("Update a Document from JSON")
    
    if request.method == 'POST' or request.method == 'PUT':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data['document']
            doc = json.loads(document)
            if not doc.has_key("_id") and not doc.has_key("id"):
                result = { "code":    400,
                           "type":    "Error",
                           "message": "Updates must include either id or _id." }
                results_json = json.dumps(result, indent = 4)
                return HttpResponse(results_json, status=result['code'],
                                    content_type="application/json")     
        
            if doc.has_key("_id") and doc.has_key("id"):
                result = { "code":    400,
                           "type":    "Error",
                           "message": "Updates cannot contain both id and _id" }
                results_json = json.dumps(result, indent = 4)
                return HttpResponse(results_json, status=result[code],
                                    content_type="application/json")     
        
            if doc.has_key("id"):
                doc["_id"] = ObjectId(doc["id"])
                del doc["id"]
                
            if doc.has_key("_id"):
                doc["_id"] = ObjectId(doc["_id"])
                

            #run the update
            results = mongo_create_json_util(document, database_name=database_name,
                                             collection_name=collection_name,
                                             update=True)
            
            #convert to json and respond.
            results_json = json.dumps(results, indent = 4)
            return HttpResponse(results_json, status=int(results['code']),
                                    content_type="application/json")        
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('djmongo/console/generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
    
    #this is a GET
    idata ={'database_name': database_name,
             'collection_name': collection_name,
             }
    

    context= {'name':name,
              'form': DocumentForm(initial=idata)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))