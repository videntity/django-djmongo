#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render, get_object_or_404
import json
import sys
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from ..decorators import (httpauth_login_required, ip_write_verification_required,
                          kickout_400, kickout_404, kickout_500)
from django.http import HttpResponse, HttpResponseRedirect
from collections import OrderedDict
from ..mongoutils import write_mongo, checkObjectId
from jsonschema import validate
from django.urls import reverse
from jsonschema.exceptions import ValidationError
from .models import WriteAPIHTTPAuth, WriteAPIIP, WriteAPIOAuth2
from .forms import (WriteAPIHTTPAuthForm, WriteAPIHTTPAuthDeleteForm,
                    WriteAPIIPDeleteForm, WriteAPIIPForm)
from .forms import WriteAPIOAuth2Form, WriteAPIOAuth2DeleteForm
from django.utils.translation import ugettext_lazy as _


def write_to_collection(request, slug, model):
    try:
        wapi = model.objects.get(slug=slug)
    except model.DoesNotExist:
        return kickout_404(
            "The API was not not found. Perhaps you need to define it?")
    if request.method == 'GET':
        return HttpResponse(
            json.dumps(wapi.http_get_response(), indent=4),
            content_type="application/json")

    # ----------------------------------------------------
    if request.method not in wapi.http_methods():
        msg = "The HTTP method %s is not allowed." % (request.method)
        return kickout_400(msg)

    if request.method in ('POST', 'PUT'):

        # Check if request body is JSON ------------------------
        try:
            j = json.loads(request.body.decode(),
                           object_pairs_hook=OrderedDict)
            if not isinstance(j, type(OrderedDict())):
                kickout_400(
                    "The request body did not contain a JSON object i.e. {}.")
        except:
            print(str(sys.exc_info()))
            return kickout_400("The request body did not contain valid JSON.")

        # Make sure that an update (PUT) contains an id or _id
        if request.method == "PUT":
            if "id" not in j.keys() and "_id" not in j.keys():
                return kickout_400("The PUT update request did not contain an id or _id.")
        # Check that id is valid:
        if j.get("id", ""):
            if not checkObjectId(j.get("id", "")):
                return kickout_400("The id was not a valid ObjectId. It must be a 12-byte input or a 24-character hex string.")

        # check json_schema is valid
        try:
            json_schema = json.loads(
                wapi.json_schema, object_pairs_hook=OrderedDict)

        except:
            print(str(sys.exc_info()))
            return kickout_500(
                "The JSON Schema on the server did not contain valid JSON.")

        # Check jsonschema
        if json_schema:
            try:
                validate(j, json_schema)
            except ValidationError:
                msg = "JSON Schema conformance error. %s" % (
                    str(sys.exc_info()[1][0]))
                return kickout_400(msg)
        # write_to_mongo

        if request.method == "POST":
            response = write_mongo(j, wapi.database_name, wapi.collection_name)
        if request.method == "PUT":
            response = write_mongo(j, wapi.database_name,
                                   wapi.collection_name, update=True)
        return HttpResponse(json.dumps(response, indent=4),
                            content_type="application/json")


@csrf_exempt
@httpauth_login_required
def write_to_collection_httpauth(request, slug):
    print("REFACTOR!!")
    return write_to_collection(request, slug, WriteAPIHTTPAuth)


@csrf_exempt
@ip_write_verification_required
def write_to_collection_ip_auth(request, slug):
    print("REFACTOR!!")
    return write_to_collection(request, slug, WriteAPIIP)


def browse_ip_write_apis(request, database_name=None, collection_name=None):
    """Deprecated"""
    name = "Write APIs Using IP-based Authentication"
    if database_name and collection_name:
        wapis = WriteAPIIP.objects.filter(
            database_name=database_name,
            collection_name=collection_name)
    else:
        wapis = WriteAPIIP.objects.all()
    context = {'name': name, 'wapis': wapis,
               'database_name': database_name,
               'collection_name': collection_name}
    return render(
        request,
        'djmongo/console/browse-ip-write-apis.html',
        context)


def browse_httpauth_write_apis(
        request,
        database_name=None,
        collection_name=None):
    """Deprecated"""
    name = "Write APIs Using HTTPAuth Authentication"
    if database_name and collection_name:
        wapis = WriteAPIHTTPAuth.objects.filter(
            database_name=database_name,
            collection_name=collection_name)
    else:
        wapis = WriteAPIHTTPAuth.objects.all()
    context = {'name': name, 'wapis': wapis,
               'database_name': database_name,
               'collection_name': collection_name}
    return render(
        request,
        'djmongo/console/browse-httpauth-write-apis.html',
        context)


def create_httpauth_write_api(
        request,
        database_name=None,
        collection_name=None):
    name = _("Create an HTTP Auth Write API")
    if request.method == 'POST':
        form = WriteAPIHTTPAuthForm(request.POST)
        if form.is_valid():
            a = form.save()
            msg = _('The HTTP Auth write API for %s was created.') % (a.slug)
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
               'form': WriteAPIHTTPAuthForm(initial=idata)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


def create_ip_write_api(request, database_name=None, collection_name=None):
    name = _("Create an IP-based Write API")
    if request.method == 'POST':
        form = WriteAPIIPForm(request.POST)
        if form.is_valid():
            a = form.save()
            msg = _('The IP-based write API for %s was created.') % (a.slug)
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
    idata = {'database_name': database_name,
             'collection_name': collection_name}
    context = {'name': name,
               'form': WriteAPIIPForm(initial=idata)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


def edit_httpauth_write_api(request, slug):
    a = get_object_or_404(WriteAPIHTTPAuth, slug=slug)
    name = _("Edit HTTP Auth Write API")
    if request.method == 'POST':
        form = WriteAPIHTTPAuthForm(request.POST, instance=a)
        if form.is_valid():
            a = form.save()
            msg = _('The HTTP Auth API for %s was updated.') % (slug)
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
               'form': WriteAPIHTTPAuthForm(instance=a)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


def edit_ip_write_api(request, slug):
    a = get_object_or_404(WriteAPIIP, slug=slug)
    name = _("Edit IP-based Write API")
    if request.method == 'POST':
        form = WriteAPIIPForm(request.POST, instance=a)
        if form.is_valid():
            a = form.save()
            msg = _('The IP-based API for %s was updated.') % (slug)
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
               'form': WriteAPIIPForm(instance=a)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


def delete_httpauth_write_api(request, slug):
    name = _("Delete HTTP Auth Write API")
    if request.method == 'POST':
        form = WriteAPIHTTPAuthDeleteForm(request.POST)
        if form.is_valid():
            a = WriteAPIHTTPAuth.objects.get(slug=slug)
            a.delete()
            msg = _('The HTTP Auth API for %s was deleted.') % (slug)
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
               'form': WriteAPIHTTPAuthDeleteForm()
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


def delete_ip_write_api(request, slug):
    name = _("Delete IP-based Write API")
    if request.method == 'POST':
        form = WriteAPIIPDeleteForm(request.POST)
        if form.is_valid():
            a = WriteAPIIP.objects.get(slug=slug)
            a.delete()
            msg = _('The IP-based API for %s was deleted.') % (slug)
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
               'form': WriteAPIIPDeleteForm()
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context,
    )


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
            msg = _('The OAuth2 write API for %s was created.') % (a.slug)
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
