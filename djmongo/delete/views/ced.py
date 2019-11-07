#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from ..models import HTTPAuthDeleteAPI, PublicDeleteAPI, OAuth2DeleteAPI, IPAuthDeleteAPI
from collections import OrderedDict
from ..forms import HTTPAuthDeleteAPIForm, IPAuthDeleteAPIForm, OAuth2DeleteAPIForm, PublicDeleteAPIForm

model_map = OrderedDict()

model_map["public"] = {"model": PublicDeleteAPI,
                       "name": "Public Delete API",
                       "form": PublicDeleteAPIForm}

model_map["httpauth"] = {"model": HTTPAuthDeleteAPI,
                         "name": "HTTP Auth Delete API",
                         "form": HTTPAuthDeleteAPIForm}

model_map["ipauth"] = {"model": IPAuthDeleteAPI,
                       "name": "IP Auth Delete API",
                       "form": HTTPAuthDeleteAPIForm}

model_map["oauth2"] = {"model": OAuth2DeleteAPI,
                       "name": "OAuth2 Delete API",
                       "form": OAuth2DeleteAPIForm}


def create_delete_api(request, auth_type, database_name, collection_name):

    if auth_type not in model_map.keys():
        raise Http404

    mymodel = model_map[auth_type]['model']
    myform = model_map[auth_type]['form']
    name = "Create a %s" % (model_map[auth_type]['name'])

    if request.method == 'POST':
        form = myform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("The %s was created." % (name)))

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
               'form': form(initial=idata)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_delete_api(request, auth_type, database_name, collection_name, slug):
    pass


def delete_delete_api(request, auth_type, database_name, collection_name, slug):
    pass
