#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render, get_object_or_404
import json
import sys
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from ..decorators import (httpauth_login_required, ip_verification_required,
                          kickout_400, kickout_404, kickout_500)
from django.http import HttpResponse, HttpResponseRedirect
from collections import OrderedDict
from ..mongoutils import write_mongo
from jsonschema import validate
from django.core.urlresolvers import reverse
from jsonschema.exceptions import ValidationError
from .models import WriteAPIOAuth2
from .forms import WriteAPIOAuth2Form, WriteAPIOAuth2DeleteForm
from django.utils.translation import ugettext_lazy as _







@csrf_exempt
def write_to_collection_oauth2(request, slug):
    
    try:
        wapi = WriteAPIOAuth2.objects.get(slug=slug)
    except WriteAPIOAuth2.DoesNotExist:
        return kickout_404(
            "The API was not not found. Perhaps you need to define it?")

    # ----------------------------------------------------
    if request.method == 'GET':
        try:
            od = OrderedDict()
            od["http_methods"] = wapi.http_methods()
            od["slug"] = wapi.slug
            od["auth_method"] = "oauth2"
            od["json_schema"] = json.loads(wapi.json_schema,
                                           object_pairs_hook=OrderedDict)
            od["readme"] =  wapi.readme_md
            return HttpResponse(
                json.dumps(od, indent=4),
                content_type="application/json")
        except:
            return kickout_500("The JSON Schema did not contain valid JSON")

    # ----------------------------------------------------
    if request.method in ('POST', 'PUT'):

        # Check if request body is JSON ------------------------
        try:
            j = json.loads(request.body.decode(), object_pairs_hook=OrderedDict)
            if not isinstance(j, type(OrderedDict())):
                kickout_400(
                    "The request body did not contain a JSON object i.e. {}.")
        except:
            print(str(sys.exc_info()))
            return kickout_400("The request body did not contain valid JSON.")

        # check json_schema is valid
        try:
            json_schema = json.loads(
                wapi.json_schema, object_pairs_hook=OrderedDict)
        except:
            print(str(sys.exc_info()))
            return kickout_500(
                "The JSON Schema on the server did not contain valid JSON")

        # Check jsonschema
        if json_schema:
            try:
                validate(j, json_schema)
            except ValidationError:
                msg = "JSON Schema Conformance Error. %s" % (
                    str(sys.exc_info()[1][0]))
                return kickout_400(msg)
        # write_to_mongo
        
        if request.method == "POST":
            response = write_mongo(j, wapi.database_name, wapi.collection_name)
        elif request.method == "GET":
            response = write_mongo(j, wapi.database_name, wapi.collection_name, update=True)
        return HttpResponse(json.dumps(response, indent=4),
                            content_type="application/json")
    
def create_oauth2_write_api(
        request,
        database_name=None,
        collection_name=None):
    name = _("Create an OAuth2 Write API")
    if request.method == 'POST':
        form = WriteAPIOAuth2Form(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.created_by = request.user
            a.save()
            msg = _('The HTTP OAuth2 write API for %s was created.') % (a.slug)
            messages.success(request, msg)

            return HttpResponseRedirect(reverse('djmongo_show_apis',
                                                args=(a.database_name,
                                                      a.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            context = {'form': form, 'name': name}
            return render(
                request,
                'djmongo/console/generic/bootstrapform.html',
                context)

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}
    context = {'name': name,
               'form': WriteAPIOAuth2Form(initial=idata)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )



def edit_oauth2_write_api(request, slug):
    a = get_object_or_404(WriteAPIOAuth2, slug=slug)
    name = _("Edit OAuth2 Write API")
    if request.method == 'POST':
        form = WriteAPIOAuth2Form(request.POST, instance=a)
        if form.is_valid():
            a = form.save(commit=False)
            a.created_by = request.user
            a.save()
            msg = _('The OAuth2 API for %s was updated.') % (slug)
            messages.success(request, msg)
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(a.database_name,
                              a.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            context = {'form': form, 'name': name}
            return render(
                request,
                'djmongo/console/generic/bootstrapform.html',
                context)
    # this is a GET
    context = {'name': name,
               'form': WriteAPIOAuth2Form(instance=a)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


def delete_oauth2_write_api(request, slug):
    name = _("Delete OAuth2 Write API")
    if request.method == 'POST':
        form = WriteAPIOAuth2DeleteForm(request.POST)
        if form.is_valid():
            a = WriteAPIOAuth2.objects.get(slug=slug)
            database_name = a.database_name
            collection_name = a.collection_name
            a.delete()
            msg = _('The OAuth2 API for %s was deleted.') % (slug)
            messages.success(request, msg)
            return HttpResponseRedirect(
                reverse('djmongo_show_apis',
                        args=(a.database_name,
                              a.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            context = {'form': form, 'name': name}
            return render(
                request,
                'djmongo/console/generic/bootstrapform.html',
                context)

    # this is a GET
    context = {'name': name,
               'form': WriteAPIOAuth2DeleteForm()
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )
