#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from .utils import (
    show_dbs,
    mongodb_drop_collection,
    mongodb_drop_database,
    mongo_delete_json_util,
    mongo_create_json_util)
from .forms import (EnsureIndexForm, DeleteForm, DocumentForm,
                    CreateDatabaseForm, ConfirmDropForm)
from bson.objectid import ObjectId
from collections import OrderedDict
from ..write.models import WriteAPIHTTPAuth, WriteAPIIP
from ..search.models import (CustomHTTPAuthReadAPI, CustomPublicReadAPI,
                             HTTPAuthReadAPI, PublicReadAPI)


def show_apis(request, database_name, collection_name):

    # Get all of the Read APIs
    custom_httpauth_read_apis = CustomHTTPAuthReadAPI.objects.filter(
        database_name=database_name, collection_name=collection_name)
    custom_public_read_apis = CustomPublicReadAPI.objects.filter(
        database_name=database_name, collection_name=collection_name)

    simple_public_read_apis = PublicReadAPI.objects.filter(
        database_name=database_name, collection_name=collection_name)
    simple_httpauth_read_apis = HTTPAuthReadAPI.objects.filter(
        database_name=database_name, collection_name=collection_name)

    # Get all of the Write APIs
    ip_write_apis = WriteAPIIP.objects.filter(database_name=database_name,
                                              collection_name=collection_name)
    httpauth_write_apis = WriteAPIHTTPAuth.objects.filter(
        database_name=database_name, collection_name=collection_name)

    context = {"custom_httpauth_read_apis": custom_httpauth_read_apis,
               "custom_public_read_apis": custom_public_read_apis,
               "simple_public_read_apis": simple_public_read_apis,
               "simple_httpauth_read_apis": simple_httpauth_read_apis,
               "httpauth_write_apis": httpauth_write_apis,
               "ip_write_apis": ip_write_apis,
               'database_name': database_name,
               'collection_name': collection_name}
    return render(request, 'djmongo/console/show-apis.html',
                  context)


def showdbs(request):

    dbs = show_dbs()
    # print(json.dumps(dbs, indent=4))
    cleaned_dbs = []
    if not dbs:
        messages.error(
            request,
            _("""Unable to connect to MongoDB.
              Check that it is running and accessible."""))
    else:
        for i in dbs:
            # only keep non-system DBs.
            if i.get('name', '') != 'admin' and i.get('name', '') != 'local':
                cleaned_dbs.append(i)

    if dbs and not cleaned_dbs:
        messages.info(
            request,
            _("""You have no databases to work on. Please create one."""))

    #     #We have data so let's grab all APIs
    #     apis = []
    #
    #     # Get all of the APIs.
    #     for d in cleaned_dbs:
    #         for c in d['collections']:
    #             # databse_name, collection_name, APIType, AuthType, HTTP Method, object
    #             # new row
    #             api = []
    #             # database name 0
    #             database_name = d['name']
    #             api.append(database_name)
    #
    #             # collection name 1
    #             api.append(c)
    #
    #             # API Type 2
    #             api.append('Basic')
    #
    #             # AuthType 3
    #             api.append("None")
    #
    #             # HTTP Method 4
    #             api.append("GET")
    #
    #             # Read Public
    #             read_public_list = PublicReadAPI.objects.filter(database_name = database_name,
    #                                                collection_name = c)
    #
    #
    #             database['apis'].append(api)
    #
    #             # HTTPAuth Read
    #             api = {}
    #             api['read_httpauth'] = HTTPAuthReadAPI.objects.filter(database_name = database_name,
    #                                                collection_name = c)
    #             database['apis'].append(api)
    #
    #             # Write Httpauth
    #             api = {}
    #             api['write_httpauth'] = WriteAPIHTTPAuth.objects.filter(database_name = database_name,
    #                                                collection_name = c)
    #             database['apis'].append(api)
    #
    #             # Write IP Auth
    #             api = {}
    #             api['write_ip_auth'] = WriteAPIIP.objects.filter(database_name = database_name,
    #                                                collection_name = c)
    #             database['apis'].append(api)
    #
    #             # Custom Read http Auth
    #             api = {}
    #             api['custom_read_httpauth'] = SavedSearch.objects.filter(database_name = database_name,
    #                                                collection_name = c)
    #             database['apis'].append(api)                #collection[c].append(api)
    #         apis.append(database)
    #
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(apis)

    context = {"dbs": cleaned_dbs}
    return render(request, 'djmongo/console/showdbs.html', context)


def drop_collection(request, database_name, collection_name):
    """Drop Collection"""
    name = """Retype "%s" to drop the collection""" % (collection_name)
    if request.method == 'POST':
        form = ConfirmDropForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if name != collection_name:
                messages.error(request, _('The name did not match. \
                                         Drop operation aborted'))
                return HttpResponseRedirect(
                    reverse(
                        'djmongo_drop_collection',
                        args=(
                            database_name,
                            collection_name)))

            response = mongodb_drop_collection(database_name, collection_name)
            if response:
                errormsg = _("ERROR", response)
                messages.error(request, errormsg)
                return HttpResponseRedirect(reverse('djmongo_show_dbs'))
            else:
                messages.success(request, _("The collection was deleted."))
                return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})
    # This is a GET
    context = {'name': name,
               'form': ConfirmDropForm(
                   initial={})}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def drop_database(request, database_name):
    name = """Retype "%s" to drop the database""" % (database_name)
    if request.method == 'POST':
        form = ConfirmDropForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if name != database_name:
                messages.error(request, _('The name did not match. \
                                         Drop operation aborted.'))
                return HttpResponseRedirect(reverse('show_dbs'))

            response = mongodb_drop_database(database_name)
            if response:
                errormsg = _("ERROR", response)
                messages.error(request, errormsg)
                return HttpResponseRedirect(reverse('djmongo_show_dbs'))
            else:
                messages.success(request, _("The database was deleted."))
                return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})
    # This is a GET
    context = {'name': name,
               'form': ConfirmDropForm(
                   initial={})}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def simple_ensure_index(request, database_name, collection_name):
    """Ensure a MongoDB index on a particular field name"""
    name = "Ensure a MongoDB index on a particular field name"

    if request.method == 'POST':
        form = EnsureIndexForm(request.POST)

        if form.is_valid():
            result = form.save(database_name, collection_name)
            messages.success(request,
                             _("Index for %s created successfully" % result))
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})

    else:
        # this is a GET
        context = {'name': name,
                   'form': EnsureIndexForm(
                       initial={"database_name": database_name,
                                "collection_name": collection_name})
                   }
        return render(request, 'djmongo/console/generic/bootstrapform.html',
                      context)


def create_new_database(request):
    """Create a New Mongo Database by adding a single document."""
    name = "Create a New MongoDB Database"

    if request.method == 'POST':
        form = CreateDatabaseForm(request.POST)

        if form.is_valid():
            result = form.save()
            if "error" in result:
                messages.error(
                    request, "The database creation operation failed.")
                messages.error(request, result["error"])
            else:
                messages.success(request, "Database created.")
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name})

    else:
        # this is a GET
        context = {'name': name,
                   'form': CreateDatabaseForm(
                       initial={"initial_document": '{ "foo" : "bar" }'
                                })
                   }
        return render(request, 'djmongo/console/generic/bootstrapform.html',
                      context)


def create_collection(request, database_name):
    """Create a new MongoDB collection by adding a single document."""
    name = "Create a New Collection"

    if request.method == 'POST':
        form = CreateDatabaseForm(request.POST)

        if form.is_valid():
            result = form.save()
            if "error" in result:
                messages.error(
                    request, _("The database creation operation failed."))
                messages.error(request, result["error"])
            else:
                messages.success(request, "Collection created.")
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})

    else:
        # this is a GET
        context = {'name': name,
                   'form': CreateDatabaseForm(
                       initial={"initial_document": '{ "foo" : "bar" }',
                                "database_name": database_name})
                   }
        return render(request, 'djmongo/console/generic/bootstrapform.html',
                      context)


def remove_data_from_collection(request, database_name, collection_name):

    name = _("""Delete select information from a MongoDB Collection
             based on a query""")

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            just_one = form.cleaned_data['just_one']

            # run the delete
            results = mongo_delete_json_util(
                query,
                database_name=database_name,
                collection_name=collection_name,
                just_one=just_one)

            # convert to json and respond.
            results_json = json.dumps(results, indent=4)
            return HttpResponse(results_json, status=int(results['code']),
                                content_type="application/json")
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': DeleteForm(initial=idata)}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_document_in_collection(request, database_name, collection_name):
    name = _("Create a Document from JSON")

    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data['document']
            # create the document
            results = mongo_create_json_util(document,
                                             database_name=database_name,
                                             collection_name=collection_name)

            # convert to json and respond.
            results_json = json.dumps(results, indent=4)
            return HttpResponse(results_json,
                                status=int(results['code']),
                                content_type="application/json")
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name})
    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name, 'form': DocumentForm(initial=idata)}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def update_document_in_collection(request, database_name, collection_name):
    name = _("Update a Document from JSON")

    if request.method == 'POST' or request.method == 'PUT':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data['document']
            doc = json.loads(document, object_pairs_hook=OrderedDict)
            if "_id" not in doc and "id" not in doc:
                result = {"code": 400, "type": "Error", "message": _(
                    "Updates must include either id or _id.")}
                results_json = json.dumps(result, indent=4)
                return HttpResponse(results_json, status=result['code'],
                                    content_type="application/json")

            if "_id" in doc and "id" in doc:
                result = {"code": 400, "type": "Error", "message": _(
                    "Updates cannot contain both id and _id")}
                results_json = json.dumps(result, indent=4)
                return HttpResponse(results_json, status=result['code'],
                                    content_type="application/json")

            if "id" in doc:
                doc["_id"] = ObjectId(doc["id"])
                del doc["id"]

            if "_id" in doc:
                doc["_id"] = ObjectId(doc["_id"])

            # run the update
            results = mongo_create_json_util(
                document,
                database_name=database_name,
                collection_name=collection_name,
                update=True)

            # convert to json and respond.
            results_json = json.dumps(results, indent=4)
            return HttpResponse(results_json, status=int(results['code']),
                                content_type="application/json")
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': DocumentForm(initial=idata)}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)
