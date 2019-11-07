#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import AggregationForm
from .models import Aggregation
from django.utils.translation import ugettext_lazy as _


def create_saved_aggregation(request, database_name=None,
                             collection_name=None):
    name = _("Create a Saved Aggregation")
    if request.method == 'POST':
        form = AggregationForm(request.POST)
        if form.is_valid():
            sa = form.save(commit=False)
            sa.user = request.user
            sa.save()

            return HttpResponseRedirect(
                reverse(
                    'djmongo_browse_saved_aggregations_w_params',
                    args=(
                        sa.database_name,
                        sa.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request,
                          'djmongo/console/generic/bootstrapform.html',
                          {'form': form,
                           'name': name},
                          )

    # This is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': AggregationForm(initial=idata)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context)


def run_aggregation_by_slug(request, slug):
    """Run Aggregation By Slug"""
    sa = get_object_or_404(Aggregation, slug=slug)
    sa.execute_now = True
    sa.save()
    messages.success(request, _("Saved aggregation executed."))
    return HttpResponseRedirect(
        reverse(
            'djmongo_browse_saved_aggregations_w_params',
            args=(
                sa.database_name,
                sa.collection_name)))


def delete_saved_aggregation_by_slug(request, slug):
    """Delete Saved Aggregation By Slug"""
    ss = get_object_or_404(Aggregation, slug=slug)
    ss.delete()
    messages.success(request, _("Saved aggregation deleted."))
    return HttpResponseRedirect(
        reverse(
            'djmongo_browse_saved_aggregations_w_params',
            args=(
                ss.database_name,
                ss.collection_name)))


def edit_saved_aggregation_by_slug(request, slug):
    name = _("Edit Saved Aggregation")
    ss = get_object_or_404(Aggregation, slug=slug, user=request.user)

    if request.method == 'POST':
        form = AggregationForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save(commit=False)
            ss.user = request.user
            ss.save()
            messages.success(request, _("Aggregation edit saved."))
            return HttpResponseRedirect(
                reverse(
                    'djmongo_browse_saved_aggregations_w_params',
                    args=(
                        ss.database_name,
                        ss.collection_name)))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request, 'generic/bootstrapform.html',
                          {'form': form,
                           'name': name,
                           })
    # this is a GET
    context = {'name': name,
               'form': AggregationForm(instance=ss)
               }
    return render(
        request,
        'djmongo/console/generic/bootstrapform.html',
        context)


def browse_saved_aggregations(request, database_name, collection_name):

    savedaggs = Aggregation.objects.filter(
        database_name=database_name,
        collection_name=collection_name)
    context = {"savedaggs": savedaggs,
               'database_name': database_name,
               'collection_name': collection_name}
    return render(
        request,
        'djmongo/console/display-saved-aggregations.html',
        context)
