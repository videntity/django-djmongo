#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import os, uuid, json
from django.conf import settings
from ..decorators import check_database_access
from django.shortcuts import render_to_response,  get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from forms import SavedSearchForm, ComplexSearchForm, AggregationForm
from ..mongoutils import query_mongo, to_json, normalize_results
from models import SavedSearch, Aggregation
from xls_utils import convert_to_csv, convert_to_rows
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
import shlex


def build_keys(request):
    """Perform the map/reduce to refresh the keys form. The display the custom report screen"""
    x = build_keys_with_mapreduce()
    messages.success(request, "Successfully completed MapReduce operation. Key rebuild for custom report complete.")
    return HttpResponseRedirect(reverse("djmongo_home"))



def prepare_search_results(request, database_name, collection_name,
                skip=0, sort=None, limit=getattr(settings, 'MONGO_LIMIT', 200), return_keys=(), query={}):
    if not query:
        kwargs = {}
        for k,v in request.GET.items():
            kwargs[k]=v
            if kwargs.has_key('limit'):
                limit=int(kwargs['limit'])
                del kwargs['limit']
            if kwargs.has_key('skip'):
                skip=int(kwargs['skip'])
                del kwargs['skip']
    else:
        kwargs = query
    

    result = query_mongo(database_name, collection_name, query=kwargs, skip=skip, limit=limit,
                         sort=sort, return_keys=return_keys)

    return result
    

@csrf_exempt
def custom_report(request, database_name, collection_name):
    ckeys = get_collection_keys()

    if request.method == 'POST':
        form = KeysForm(ckeys, get_collection_labels(), request.POST)
        if form.is_valid():
            return_keys=[]
            data = form.cleaned_data
            for k,v in data.items():
                if v==True:
                    return_keys.append(k)

            q = massage_dates(json.loads(data['query']))

            if data['outputformat']=="xls":
                return search_xls(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))
            
            elif data['outputformat']=="csv":
                return search_csv(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))
            
            elif data['outputformat']=="xml":
                return search_xml(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))
            else:
                return search_json(request, collection=None, return_keys=return_keys,
                                   query=json.loads(data['query']))

        else:

            return render_to_response('search/select-keys.html', {'form': form},
                RequestContext(request))

    #Get the distinct keys from the collection
    ckeys = get_collection_keys()

    #get the labels
    label_dict = get_collection_labels()

    return render_to_response('djmongo/console/select-keys.html',
         {'form': KeysForm(ckeys, label_dict),}, RequestContext(request))



@check_database_access
def search_json(request, database_name,collection_name,
                skip=0, limit=getattr(settings,'MONGO_LIMIT', 200), sort=None, return_keys=(),
                query={}):
    

    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, skip=skip, sort=sort,
                limit=limit, return_keys=return_keys, query=query)

    if int(result['code'])==200:
        listresults=result['results']

    else:
        response = json.dumps(result, indent =4)
        return HttpResponse(response, status=int(result['code']),
                            content_type="application/json")

    jsonresults=to_json(normalize_results(result))
    return HttpResponse(jsonresults, status=int(result['code']),content_type="application/json")


@check_database_access
def search_csv(request, database_name,collection_name,
                skip=0, sort=None, limit=getattr(settings,'MONGO_LIMIT', 200),
                return_keys=(), query={}):
    
    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, sort=sort, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    #print result.keys()

    if int(result['code']) == 200:
        listresults=result['results']
        keylist = []
        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)


        return convert_to_csv(keylist, listresults)

    else:
        jsonresults=to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            content_type="application/json")


@check_database_access
def search_html(request, database_name, collection_name,
                sort=None, skip=0, limit=getattr(settings,'MONGO_LIMIT', 200),
                return_keys=(),
                query={}):
    
    
    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S UTC')    
    result = prepare_search_results(request, database_name=database_name,
                collection_name=collection_name, sort=sort, skip=skip,
                limit=limit, return_keys=return_keys, query=query)

    #print result.keys()

    if int(result['code']) == 200:
        listresults=result['results']

        keylist = []
        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)
        context ={"rows": convert_to_rows(keylist, listresults),
                  "timestamp": timestamp}
        
        return render_to_response('djmongo/console/html-table.html',
                              RequestContext(request, context,))   

    else:
        jsonresults=to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            content_type="application/json")



@csrf_exempt
def data_dictionary(request):

    if request.method == 'POST':
        form = DataDictionaryForm(request.POST)
        if form.is_valid():
            data = form.save()

            if data['outputformat']=="xls":
                pass
                #return convert_labels_to_xls(data)

            else:
                response = json.dumps(data['labels'], indent =4)
                return HttpResponse(response, status=200,
                                    content_type="application/json")
        else:
            #The form contained errors.
            return render_to_response('search/data-dictionary.html',
                                 {'form': form}, RequestContext(request))

    #A GET
    return render_to_response('search/data-dictionary.html',
         {'form': DataDictionaryForm()}, RequestContext(request))


@csrf_exempt
def load_labels(request):

    labels = get_labels_tuple()

    for i in labels:
        variable = strip_occurences(i[0])
        try:
            DataLabelMeta.objects.create(variable_name=variable,
                                          verbose_name=i[1],
                                          label=i[1],)
        except(IntegrityError):
            l =  DataLabelMeta.objects.get(variable_name=variable)
            l.verbose_name = i[1]
            l.label=i[1]
            l.question_text=i[1]
            l.save()
    return HttpResponse("OK")

    if request.method == 'POST':
        form = DataDictionaryForm(request.POST)
        if form.is_valid():
            data = form.save()

            if data['outputformat']=="xls":
                pass
                #return convert_labels_to_xls(data)

            else:
                response = json.dumps(data['labels'], indent =4)
                return HttpResponse(response, status=200,
                                    content_type="application/json")
        else:
            #The form contained errors.
            return render_to_response('djmongo/console/data-dictionary.html',
                                 {'form': form}, RequestContext(request))

    #A GET
    return render_to_response('djmongo/console/data-dictionary.html',
         {'form': DataDictionaryForm()}, RequestContext(request))



def run_saved_search_by_slug(request, slug, output_format=None, skip=0,
                             sort=None, limit = getattr(settings,'MONGO_LIMIT', 200)):
    
    error = False
    response_dict = {}
    ss = get_object_or_404(SavedSearch,  slug=slug)
    #Don't run the search unless its public.
    
    if not request.user.is_authenticated() and not ss.is_public:
        response_dict = {}
        response_dict['num_results']=0
        response_dict['code']=401
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']="Not Found. Perhaps you need to log in?"
        response = json.dumps(response_dict, indent =4)
        return HttpResponse(response, content_type="application/json")
    elif not request.user.groups.filter(name__in=[ss.group,]).exists() and not ss.is_public:
            response_dict = {}
            response_dict['num_results']=0
            response_dict['code']=401
            response_dict['type']="Error"
            response_dict['results']=[]
            response_dict['message']="You do not have permission to run this search."
            response = json.dumps(response_dict, indent =4)
            return HttpResponse(response, content_type="application/json")
        
    
    query = ss.query
    #if a GET param matches, then replace it
    
    for k,v in request.GET.items():
       if k in query:
        quoted_value = '"%s"' % (v)
        query = query.replace(k, quoted_value)
    
    try:
        query = json.loads(query)
        if ss.sort:
            #print ss.sort
            sort = json.loads(ss.sort)
 
 
    except ValueError:
        response_dict = {}
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']="Your query was not valid JSON."
        response = json.dumps(response_dict, indent =4)
        return HttpResponse(response, content_type="application/json")


    if output_format:
        if output_format not in ("json", "csv", "html"):
            response_dict['message']="The output format must be json, csv, or html."
            error = True
        else:
            ss.output_format=output_format
    try:
        skip = int(skip)
    except ValueError:
        response_dict['message']="Skip must be an integer."
        error = True
    try:
        limit = int(limit)
        
    except ValueError:
        response_dict['message']= "Limit must be an integer."
        error = True
    if error:
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response = json.dumps(response_dict, indent =4)
        return HttpResponse(response,
                content_type="application/json")
    
    
    #setup the list of keys for return if specified.
    key_list=()
    if ss.return_keys:  
        key_list = shlex.split(ss.return_keys)
    #print ss.query, ss.database_name, ss.collection_name
    
    if ss.output_format=="json":
        return search_json(request, database_name=ss.database_name,
                           collection_name =ss.collection_name,
                           sort=sort,
                           query = query, skip=int(skip), limit=int(ss.default_limit),
                           return_keys= key_list)
    

    if ss.output_format=="html":
        return search_html(request,
                          database_name=ss.database_name,
                          collection_name =ss.collection_name,
                          sort=sort,
                          query = query, skip=int(skip), limit=int(ss.default_limit),
                          return_keys= key_list) 
    

    if ss.output_format=="csv":
        return search_csv(request,
                          database_name=ss.database_name,
                           collection_name =ss.collection_name,
                          query = query, skip=int(skip), limit=int(ss.default_limit),
                           return_keys= key_list)
    
    
    #these next line "should" never execute.
    response_dict                 = {}
    response_dict['num_results']  = 0
    response_dict['code']         = 500
    response_dict['type']         = "Error"
    response_dict['results']      = []
    response_dict['message']      = "Something has gone wrong." + response_dict['message']
    response = json.dumps(response_dict, indent =4)
    return HttpResponse(response, content_type="application/json")



def create_saved_aggregation(request, database_name=None,
                collection_name=None):
    name = _("Create a Saved Aggregation")
    if request.method == 'POST':
        form = AggregationForm(request.POST)
        if form.is_valid():
            sa = form.save(commit = False)
            sa.user = request.user
            sa.save()
                
            return HttpResponseRedirect(reverse('djmongo_browse_saved_aggregations_w_params',
                                        args=(sa.database_name, sa.collection_name )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('djmongo/console/generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name},
                                            RequestContext(request))
            
   #this is a GET
    idata ={'database_name': database_name,
            'collection_name': collection_name}
    
    
    context= {'name':name,
              'form': AggregationForm(initial=idata)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                             RequestContext(request, context,))
    

def create_saved_search(request, database_name=None,
                collection_name=None,
                        skip=0, limit=getattr(settings,'MONGO_LIMIT', 200), return_keys=()):
    name = _("Create a Saved Search")
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            ss = form.save(commit = False)
            ss.user = request.user
            ss.save()
                
            return HttpResponseRedirect(reverse('djmongo_browse_saved_searches_w_params',
                                                args = (database_name, collection_name)))
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
            'collection_name': collection_name}
    
    
    context= {'name':name,
              'form': SavedSearchForm(initial=idata)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                             RequestContext(request, context,))
    

def delete_saved_search_by_slug(request, slug):
    name = _("Edit Saved Search")
    ss = get_object_or_404(SavedSearch,  slug=slug)
    ss.delete()
    messages.success(request,_("Saved search deleted."))
    return HttpResponseRedirect(reverse('djmongo_browse_saved_search_w_params', 
                                        args=(ss.database_name, ss.collection_name )))


def delete_saved_aggregation_by_slug(request, slug):
    name = _("Edit Saved Search")
    ss = get_object_or_404(SavedSearch,  slug=slug, user=request.user)
    ss.delete()
    messages.success(request,_("Saved aggregation deleted."))
    return HttpResponseRedirect(reverse('djmongo_browse_saved_search_w_params',
                                        args=(ss.database_name, ss.collection_name )))



def edit_saved_search_by_slug(request, slug):
    name = _("Edit Saved Search")
    ss = get_object_or_404(SavedSearch,  slug=slug)
    
    if request.method == 'POST':
        form = SavedSearchForm(request.POST, instance =ss)
        if form.is_valid():
            ss = form.save(commit = False)
            ss.user = request.user
            ss.save()
            messages.success(request,_("Saved search edit saved."))    
            return HttpResponseRedirect(reverse('djmongo_browse_saved_search_w_params',
                                        args=(ss.database_name, ss.collection_name )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
            
   #this is a GET
    context= {'name':name,
              'form': SavedSearchForm(instance = ss)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                             RequestContext(request, context,))




def delete_saved_search_by_slug(request, slug):
    name = _("Edit Saved Search")
    ss = get_object_or_404(SavedSearch,  slug=slug)
    ss.delete()
    messages.success(request,_("Saved search deleted."))
    return HttpResponseRedirect(reverse('djmongo_browse_saved_search_w_params',
                                        args=(ss.database_name, ss.collection_name )))



def run_aggregation_by_slug(request, slug):
    name = _("Execute Aggregation")
    sa = get_object_or_404(Aggregation,  slug=slug)
    sa.execute_now = True
    sa.save()
    messages.success(request,_("Saved aggregation executed."))
    return HttpResponseRedirect(reverse('djmongo_browse_saved_aggregations_w_params',
                                        args=(sa.database_name, sa.collection_name )))



def delete_saved_aggregation_by_slug(request, slug):
    name = _("Edit Saved Search")
    ss = get_object_or_404(Aggregation,  slug=slug)
    ss.delete()
    messages.success(request,_("Saved aggregation deleted."))
    return HttpResponseRedirect(reverse('djmongo_browse_saved_aggregations_w_params',
                                        args=(ss.database_name, ss.collection_name )))



def edit_saved_aggregation_by_slug(request, slug):
    name = _("Edit Saved Aggregation")
    ss = get_object_or_404(Aggregation,  slug=slug, user=request.user)
    
    if request.method == 'POST':
        form = AggregationForm(request.POST, instance =ss)
        if form.is_valid():
            ss = form.save(commit = False)
            ss.user = request.user
            ss.save()
            messages.success(request,_("Aggregation edit saved."))    
            return HttpResponseRedirect(reverse('djmongo_browse_saved_aggregations_w_params',
                                        args=(ss.database_name, ss.collection_name )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
            
   #this is a GET
    context= {'name':name,
              'form': AggregationForm(instance = ss)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                             RequestContext(request, context,))





def complex_search(request, database_name,collection_name,
                        sort=None, skip=0, limit=200, return_keys=()):
    name = _("Run a Complex Search")
    if request.method == 'POST':
        form = ComplexSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            limit = form.cleaned_data['limit']
            sort = form.cleaned_data['sort']
            try:
                query = json.loads(query)
                
                if sort:
                    sort = json.loads(sort)

            except ValueError:
                #Quert was not valid JSON ------------------
                response_dict = {}
                response_dict['num_results']=0
                response_dict['code']=400
                response_dict['type']="Error"
                response_dict['results']=[]
                response_dict['message']="Your query was not valid JSON."
                response = json.dumps(response_dict, indent =4)
                return HttpResponse(response, status=int(response_dict['code']),
                                    content_type="application/json")
            #Query was valid JSON    
            if form.cleaned_data['output_format']=="json":
                return search_json(request, query = query, sort=sort, limit=limit, skip=skip)
            if form.cleaned_data['output_format']=="csv":
                return search_csv(request, query = query, sort=sort, limit=limit, skip=skip)
            if form.cleaned_data['output_format']=="html":
                return search_html(request, query = query, sort=sort, limit=limit, skip=skip)
            
            #these next line "should" never execute, but here just in case.
            response_dict = {}
            response_dict['num_results']=0
            response_dict['code']=500
            response_dict['type']="Error"
            response_dict['results']=[]
            response_dict['message']="Oops somthing has gone wrong.  Please contact a systems administrator"
            response = json.dumps(response_dict, indent =4)
            return HttpResponse(response, status=int(response_dict['code']),
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
    
    #if the database and collection are not identified, use the main one
    # defined in settings.
    if not database_name or collection_name:
        idata ={'database_name': settings.MONGO_DB_NAME,
           'collection_name': settings.MONGO_MASTER_COLLECTION,
           }
    else:
        idata ={'database_name': database_name,
             'collection_name': collection_name,
             }
    idata['output_format'] = 'json'
    idata['query']="{}"
    
    context= {'name':name,
              'form': ComplexSearchForm(initial=idata)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                             RequestContext(request, context,))

def display_saved_searches(request, database_name, collection_name):
     
    savedsearches = SavedSearch.objects.filter(database_name=database_name, collection_name=collection_name)
    context = {"savedsearches": savedsearches,
               'database_name': database_name,
               'collection_name': collection_name}
    return render_to_response('djmongo/console/display-saved-searches.html',
                              RequestContext(request, context,))

def display_saved_aggregations(request, database_name, collection_name):
     
    savedaggs = Aggregation.objects.filter(database_name=database_name, collection_name=collection_name)
    context = {"savedaggs": savedaggs,
               'database_name': database_name,
               'collection_name': collection_name}
    return render_to_response('djmongo/console/display-saved-aggregations.html',
                              RequestContext(request, context,))
