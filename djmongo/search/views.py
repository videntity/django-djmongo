#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import json
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from .forms import (HTTPAuthReadAPIForm, PublicReadAPIForm,
                    CustomHTTPAuthReadAPIForm, CustomPublicReadAPIForm)
from ..mongoutils import (query_mongo, to_json, normalize_results,
                          build_keys_with_mapreduce)
from .models import (PublicReadAPI, HTTPAuthReadAPI,
                     CustomHTTPAuthReadAPI, CustomPublicReadAPI)
from .xls_utils import convert_to_csv, convert_to_rows
from django.utils.translation import ugettext_lazy as _
import shlex


def build_keys(request, database_name, collection_name):
    """Perform the map/reduce to refresh the keys form.
       The display the custom report screen"""
    build_keys_with_mapreduce(database_name, collection_name)
    messages.success(request, _(
        "Successfully completed MapReduce operation. "
        "Key rebuild for custom report complete."))
    return HttpResponseRedirect(reverse("djmongo_show_dbs"))


def prepare_search_results(request, database_name,
                           collection_name, skip=0,
                           sort=None, limit=getattr(settings,
                                                    'MONGO_LIMIT', 200),
                           return_keys=(),
                           query={}):
    # By default, do not include number of search results.
    include_num_results = "0"

    if not query:
        kwargs = {}
        for k, v in request.GET.items():
            kwargs[k] = v
            if 'limit' in kwargs:
                limit = int(kwargs['limit'])
                del kwargs['limit']
            if 'skip' in kwargs:
                skip = int(kwargs['skip'])
                del kwargs['skip']
            # Include search result numbers if asked.
            if 'include_num_results' in kwargs:
                include_num_results = kwargs['include_num_results']
                del kwargs['include_num_results']

    else:
        kwargs = query
    result = query_mongo(database_name,
                         collection_name,
                         query=kwargs,
                         include_num_results=include_num_results,
                         skip=skip, limit=limit,
                         sort=sort, return_keys=return_keys)
    return result


def simple_search(request, database_name, collection_name, slug, output_type,
                  skip=0, limit=getattr(settings, 'MONGO_LIMIT', 200),
                  sort=None, return_keys=(),
                  query={}):

    if output_type == "json":
        return search_json(request, database_name, collection_name,
                           skip=skip, limit=limit,
                           sort=sort, return_keys=return_keys,
                           query=query)

    if output_type == "html":
        return search_html(request, database_name, collection_name,
                           skip=skip, limit=limit,
                           sort=sort, return_keys=return_keys,
                           query=query)

    if output_type == "csv":
        return search_csv(request, database_name, collection_name,
                          skip=skip, limit=limit,
                          sort=sort, return_keys=return_keys,
                          query=query)

    raise Http404


def search_json(request, database_name, collection_name,
                skip=0, limit=getattr(settings, 'MONGO_LIMIT', 200),
                sort=None, return_keys=(),
                query={}):
    result = prepare_search_results(
        request,
        database_name=database_name,
        collection_name=collection_name,
        skip=skip,
        sort=sort,
        limit=limit,
        return_keys=return_keys,
        query=query)

    if int(result['code']) == 200:
        # listresults = result['results']
        jsonresults = to_json(normalize_results(result))
        return HttpResponse(jsonresults,
                            status=int(result['code']),
                            content_type="application/json")
    else:
        response = json.dumps(result, indent=4)
        return HttpResponse(response, status=int(result['code']),
                            content_type="application/json")


def search_csv(request, database_name, collection_name,
               skip=0, sort=None, limit=getattr(settings, 'MONGO_LIMIT', 200),
               return_keys=(), query={}):

    result = prepare_search_results(
        request,
        database_name=database_name,
        collection_name=collection_name,
        sort=sort,
        skip=skip,
        limit=limit,
        return_keys=return_keys,
        query=query)

    # print result.keys()

    if int(result['code']) == 200:
        listresults = result['results']
        keylist = []
        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)

        return convert_to_csv(keylist, listresults)

    else:
        jsonresults = to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            content_type="application/json")


def search_html(request, database_name, collection_name,
                sort=None, skip=0, limit=getattr(settings, 'MONGO_LIMIT', 200),
                return_keys=(),
                query={}):

    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S UTC')
    result = prepare_search_results(
        request,
        database_name=database_name,
        collection_name=collection_name,
        sort=sort,
        skip=skip,
        limit=limit,
        return_keys=return_keys,
        query=query)

    # print result.keys()

    if int(result['code']) == 200:
        listresults = result['results']

        keylist = []
        for i in listresults:
            for j in i.keys():
                if not keylist.__contains__(j):
                    keylist.append(j)
        context = {"rows": convert_to_rows(keylist, listresults),
                   "timestamp": timestamp}

        return render(request, 'djmongo/console/html-table.html',
                      context)

    else:
        jsonresults = to_json(result)
        return HttpResponse(jsonresults, status=int(result['code']),
                            content_type="application/json")


def run_custom_public_read_api_by_slug(
    request,
    slug,
    output_format=None,
    skip=0,
    sort=None,
    limit=getattr(
        settings,
        'MONGO_LIMIT',
        200)):
    error = False
    response_dict = {}
    ss = get_object_or_404(CustomPublicReadAPI, slug=slug)

    query = ss.query
    type_mapper = json.loads(ss.type_mapper)
    type_mapper_keys = type_mapper.keys()
    # if a GET param matches, then replace it

    for k, v in request.GET.items():
        if k in query:
            if k not in type_mapper_keys:
                quoted_value = '"%s"' % (v)
            else:
                if type_mapper[k] == "number":
                    quoted_value = '%s' % (v)
                if type_mapper[k] == "boolean":
                    if v in ('true', 'True', 'TRUE', 'T', 'Y' '1'):
                        quoted_value = 'true'
                    if v in ('false', 'False', 'F', 'FALSE', 'N', '0'):
                        quoted_value = 'false'
            query = query.replace(k, quoted_value)

    try:
        query = json.loads(query)
        if ss.sort:
                # print ss.sort
            sort = json.loads(ss.sort)

    except ValueError:
        response_dict = {}
        response_dict['num_results'] = 0
        response_dict['code'] = 400
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = "Your query was not valid JSON."
        response = json.dumps(response_dict, indent=4)
        return HttpResponse(response, content_type="application/json")

    if output_format:
        if output_format not in ("json", "csv", "html"):
            response_dict[
                'message'] = "The output format must be json, csv, or html."
            error = True
        else:
            ss.output_format = output_format
    try:
        skip = int(skip)
    except ValueError:
        response_dict['message'] = "Skip must be an integer."
        error = True
    try:
        limit = int(limit)

    except ValueError:
        response_dict['message'] = "Limit must be an integer."
        error = True
    if error:
        response_dict['num_results'] = 0
        response_dict['code'] = 400
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response = json.dumps(response_dict, indent=4)
        return HttpResponse(response,
                            content_type="application/json")

    # setup the list of keys for return if specified.
    key_list = ()
    if ss.return_keys:
        key_list = shlex.split(ss.return_keys)
    # print ss.query, ss.database_name, ss.collection_name

    if ss.output_format == "json":
        return search_json(
            request,
            database_name=ss.database_name,
            collection_name=ss.collection_name,
            sort=sort,
            query=query,
            skip=int(skip),
            limit=int(
                ss.default_limit),
            return_keys=key_list)

    if ss.output_format == "html":
        return search_html(
            request,
            database_name=ss.database_name,
            collection_name=ss.collection_name,
            sort=sort,
            query=query,
            skip=int(skip),
            limit=int(
                ss.default_limit),
            return_keys=key_list)

    if ss.output_format == "csv":
        return search_csv(
            request,
            database_name=ss.database_name,
            collection_name=ss.collection_name,
            query=query,
            skip=int(skip),
            limit=int(
                ss.default_limit),
            return_keys=key_list)

    # these next line "should" never execute.
    response_dict = {}
    response_dict['num_results'] = 0
    response_dict['code'] = 500
    response_dict['type'] = "Error"
    response_dict['results'] = []
    response_dict['message'] = "Something has gone wrong." + \
        response_dict['message']
    response = json.dumps(response_dict, indent=4)
    return HttpResponse(response, content_type="application/json")


def run_custom_httpauth_read_api_by_slug(
    request,
    slug,
    output_format=None,
    skip=0,
    sort=None,
    limit=getattr(
        settings,
        'MONGO_LIMIT',
        200)):
    error = False
    response_dict = {}
    ss = get_object_or_404(CustomHTTPAuthReadAPI, slug=slug)

    if not request.user.is_authenticated():
        response_dict = {}
        response_dict['num_results'] = 0
        response_dict['code'] = 401
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = "Not Found. Perhaps you need to log in?"
        response = json.dumps(response_dict, indent=4)
        return HttpResponse(response, content_type="application/json")
    # If a group is defined check that user is in the a group.
    elif ss.group:
        if not request.user.groups.filter(name__in=[ss.group, ]).exists():
            response_dict = {}
            response_dict['num_results'] = 0
            response_dict['code'] = 401
            response_dict['type'] = "Error"
            response_dict['results'] = []
            response_dict[
                'message'] = "You do not have permission to run this search."
            response = json.dumps(response_dict, indent=4)
            return HttpResponse(response, content_type="application/json")

    # All okay, so run the query
    query = ss.query
    type_mapper = json.loads(ss.type_mapper)
    type_mapper_keys = type_mapper.keys()
    # if a GET param matches, then replace it

    for k, v in request.GET.items():
        if k in query:
            if k not in type_mapper_keys:
                quoted_value = '"%s"' % (v)
            else:
                if type_mapper[k] == "number":
                    quoted_value = '%s' % (v)
                if type_mapper[k] == "boolean":
                    if v in ('true', 'True', 'TRUE', 'T', 'Y' '1'):
                        quoted_value = 'true'
                    if v in ('false', 'False', 'F', 'FALSE', 'N', '0'):
                        quoted_value = 'false'
            query = query.replace(k, quoted_value)

    try:
        query = json.loads(query)
        if ss.sort:
                # print ss.sort
            sort = json.loads(ss.sort)

    except ValueError:
        response_dict = {}
        response_dict['num_results'] = 0
        response_dict['code'] = 400
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = "Your query was not valid JSON."
        response = json.dumps(response_dict, indent=4)
        return HttpResponse(response, content_type="application/json")

    if output_format:
        if output_format not in ("json", "csv", "html"):
            response_dict[
                'message'] = "The output format must be json, csv, or html."
            error = True
        else:
            ss.output_format = output_format
    try:
        skip = int(skip)
    except ValueError:
        response_dict['message'] = "Skip must be an integer."
        error = True
    try:
        limit = int(limit)

    except ValueError:
        response_dict['message'] = "Limit must be an integer."
        error = True
    if error:
        response_dict['num_results'] = 0
        response_dict['code'] = 400
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response = json.dumps(response_dict, indent=4)
        return HttpResponse(response,
                            content_type="application/json")

    # setup the list of keys for return if specified.
    key_list = ()
    if ss.return_keys:
        key_list = shlex.split(ss.return_keys)
    # print ss.query, ss.database_name, ss.collection_name

    if ss.output_format == "json":
        return search_json(
            request,
            database_name=ss.database_name,
            collection_name=ss.collection_name,
            sort=sort,
            query=query,
            skip=int(skip),
            limit=int(
                ss.default_limit),
            return_keys=key_list)

    if ss.output_format == "html":
        return search_html(
            request,
            database_name=ss.database_name,
            collection_name=ss.collection_name,
            sort=sort,
            query=query,
            skip=int(skip),
            limit=int(
                ss.default_limit),
            return_keys=key_list)

    if ss.output_format == "csv":
        return search_csv(
            request,
            database_name=ss.database_name,
            collection_name=ss.collection_name,
            query=query,
            skip=int(skip),
            limit=int(
                ss.default_limit),
            return_keys=key_list)

    # these next line "should" never execute.
    response_dict = {}
    response_dict['num_results'] = 0
    response_dict['code'] = 500
    response_dict['type'] = "Error"
    response_dict['results'] = []
    response_dict['message'] = "Something has gone wrong." + \
        response_dict['message']
    response = json.dumps(response_dict, indent=4)
    return HttpResponse(response, content_type="application/json")



def create_simple_httpauth_read_api(request, database_name, collection_name):
    name = _("Create Simple Read API with Basic Auth")

    if request.method == 'POST':
        form = HTTPAuthReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Record created/updated."))

            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(database_name,
                              collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })
    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}
    context = {'name': name,
               'form': HTTPAuthReadAPIForm(initial=idata)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_simple_public_read_api(request, database_name, collection_name):
    name = _("Create Simple Read API with No Auth (Public)")

    if request.method == 'POST':
        form = PublicReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Record created/updated."))

            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(database_name,
                              collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })
    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}
    context = {'name': name,
               'form': PublicReadAPIForm(initial=idata)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_simple_api(request, auth_type, database_name, collection_name):
    if auth_type == "public":
        return create_simple_public_read_api(
            request, database_name, collection_name)

    if auth_type == "httpauth":
        return create_simple_httpauth_read_api(
            request, database_name, collection_name)
    # else
    raise Http404


def create_custom_public_read_api(
        request,
        database_name=None,
        collection_name=None,
        skip=0,
        limit=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        return_keys=()):
    name = _("Create a Custom Read API with No Auth (Public)")
    if request.method == 'POST':
        form = CustomPublicReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(database_name,
                              collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': CustomPublicReadAPIForm(initial=idata)}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_custom_httpauth_read_api(
        request,
        database_name=None,
        collection_name=None,
        skip=0,
        limit=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        return_keys=()):
    name = _("Create a Custom Saved Search with Basic Auth")
    if request.method == 'POST':
        form = CustomHTTPAuthReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(database_name,
                              collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': CustomHTTPAuthReadAPIForm(initial=idata)}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_custom_api(request, auth_type, database_name, collection_name,
                      skip=0, limit=getattr(settings, 'MONGO_LIMIT', 200),
                      return_keys=()):
    if auth_type == "public":
        return create_custom_public_read_api(
            request,
            database_name,
            collection_name,
            skip=skip,
            limit=limit,
            return_keys=return_keys)

    if auth_type == "httpauth":
        return create_custom_httpauth_read_api(
            request,
            database_name,
            collection_name,
            skip=skip,
            limit=limit,
            return_keys=return_keys)
    # else
    raise Http404


def edit_simple_public_read_api(request, database_name, collection_name, slug):
    name = _("Edit Simple Read API with No Auth (Public)")
    ss = get_object_or_404(PublicReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = PublicReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save()
            messages.success(request, _("Simple Read API Saved."))
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(ss.database_name,
                              ss.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })

    # this is a GET
    context = {'name': name,
               'form': PublicReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_simple_httpauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    name = _("Edit Simple Read API with Basic Auth")
    ss = get_object_or_404(HTTPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = HTTPAuthReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save()
            messages.success(request, _("Simple Read API Saved."))
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(ss.database_name,
                              ss.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })

    # this is a GET
    context = {'name': name,
               'form': HTTPAuthReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_custom_public_read_api(request, database_name, collection_name, slug):
    name = _("Edit Custom Read API with No Auth (Public)")
    ss = get_object_or_404(CustomPublicReadAPI, datbase_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = CustomPublicReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save()
            messages.success(request, _("Simple Read API Saved."))
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(ss.database_name,
                              ss.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })
    # this is a GET
    context = {'name': name,
               'form': CustomPublicReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_custom_httpauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    name = _("Edit Custom Basic Auth Read API")
    ss = get_object_or_404(CustomHTTPAuthReadAPI, datbase_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = CustomHTTPAuthReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save(commit=False)
            ss.user = request.user
            ss.save()
            messages.success(
                request, _("Custom HTTPAuth Read API edit saved."))
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(ss.database_name,
                              ss.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })

    # this is a GET
    context = {'name': name,
               'form': CustomHTTPAuthReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def delete_custom_public_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete CustomPublicReadAPI"""
    ss = get_object_or_404(CustomPublicReadAPI, datbase_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("Custom Public Read API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_custom_httpauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete CustomHTTPAuthReadAPI"""
    ss = get_object_or_404(CustomHTTPAuthReadAPI, datbase_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("Custom HTTPAuth Read API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_simple_public_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete Simple PublicReadAPI"""
    ss = get_object_or_404(PublicReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("Simple Public Read API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_simple_httpauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete Simple PublicReadAPI"""
    ss = get_object_or_404(HTTPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("Simple HTTP Auth Read API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def browse_custom_httpauth_read_apis(request, database_name, collection_name):

    savedsearches = CustomHTTPAuthReadAPI.objects.filter(
        database_name=database_name,
        collection_name=collection_name)
    context = {"savedsearches": savedsearches,
               'database_name': database_name,
               'collection_name': collection_name}
    return render(request, 'djmongo/console/display-saved-searches.html',
                  context)
