#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from .forms import DataImportForm
from .models import DataImport


def delete_import(request, slug):
    im = get_object_or_404(DataImport, slug=slug)
    im.delete()
    messages.success(request,
                     _("The record of the import was deleted. "
                       "No data was not removed from MongoDB."))
    return HttpResponseRedirect(reverse('show_dbs'))


def import_data_file(request, database_name=None, collection_name=None):
    name = _("Import CSV File")

    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            di = form.save(commit=False)
            di.user = request.user
            di.save()
            messages.success(request, _("The data was imported successfully."))
            return HttpResponseRedirect(reverse('djmongo_show_dbs'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form, 'name': name})

    # this is a GET

    if database_name and collection_name:
        idata = {'database_name': database_name,
                 'collection_name': collection_name}
    else:
        idata = {}
    messages.warning(
        request,
        _("""For large data imports use the command line utility csv2mongo.
          Its part of "JSON Data Tools" and can be installed with "pip install
          jdt"."""))
    context = {'name': name,
               'form': DataImportForm(initial=idata),
               }
    return render(request,
                  'djmongo/console/generic/bootstrapform.html',
                  context)


def previous_data_imports(request, database_name=None, collection_name=None):

    if not database_name or collection_name:
        dataimports = DataImport.objects.filter(database_name=database_name,
                                                collection_name=database_name)
    else:
        dataimports = DataImport.objects.all()

    context = {"dataimports": dataimports,
               "database_name": database_name,
               "collection_name": collection_name}
    return render(request,
                  'djmongo/console/previous-imports.html',
                  context)
