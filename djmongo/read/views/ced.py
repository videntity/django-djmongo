#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..forms import (HTTPAuthReadAPIForm, PublicReadAPIForm,
                     CustomHTTPAuthReadAPIForm, CustomPublicReadAPIForm,
                     IPAuthReadAPIForm, CustomIPAuthReadAPIForm,
                     OAuth2ReadAPIForm, CustomOAuth2ReadAPIForm)

from ..models import (PublicReadAPI, HTTPAuthReadAPI,
                      IPAuthReadAPI, OAuth2ReadAPI,
                      CustomHTTPAuthReadAPI, CustomPublicReadAPI,
                      CustomIPAuthReadAPI, CustomOAuth2ReadAPI)

from django.utils.translation import ugettext_lazy as _

# CREATE API VIEWS -----------------------------


def create_simple_httpauth_read_api(request, database_name, collection_name):
    name = _("Create a Read API with Basic Auth")

    if request.method == 'POST':
        form = HTTPAuthReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("The API was created."))

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


def create_simple_ipauth_read_api(request, database_name, collection_name):
    name = _("Create a Read API with IP-Based Auth")

    if request.method == 'POST':
        form = IPReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("The API was created."))

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
               'form': IPReadAPIForm(initial=idata)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_simple_oauth2_read_api(request, database_name, collection_name):
    name = _("Create a Read API with OAuth2 Authentication")

    if request.method == 'POST':
        form = OAuth2ReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("The API was created."))

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
               'form': OAuth2ReadAPIForm(initial=idata)
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

    if auth_type == "ipauth":
        return create_simple_ipauth_read_api(
            request, database_name, collection_name)

    if auth_type == "oauth2":
        return create_simple_oauth2_read_api(
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
            messages.success(
                request, _("API created."))
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
    name = _("Create a Custom Read API with Basic HTTP Auth")
    if request.method == 'POST':
        form = CustomHTTPAuthReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("API created."))
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


def create_custom_ipauth_read_api(
        request,
        database_name=None,
        collection_name=None,
        skip=0,
        limit=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        return_keys=()):
    name = _("Create a Custom Read API with IP-Based Authentication")
    if request.method == 'POST':
        form = CustomIPAuthReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("API created."))
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
                           'name': name})

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': CustomIPAuthReadAPIForm(initial=idata)}
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def create_custom_oauth2_read_api(
        request,
        database_name=None,
        collection_name=None,
        skip=0,
        limit=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        return_keys=()):
    name = _("Create a Custom Read API with IP-Based Authentication")
    if request.method == 'POST':
        form = CustomOAuth2ReadAPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("API created."))
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
                           'name': name})

    # this is a GET
    idata = {'database_name': database_name,
             'collection_name': collection_name}

    context = {'name': name,
               'form': CustomOAuth2ReadAPIForm(initial=idata)}
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

    if auth_type == "ipauth":
        return create_custom_ipauth_read_api(
            request,
            database_name,
            collection_name,
            skip=skip,
            limit=limit,
            return_keys=return_keys)

    if auth_type == "oauth2":
        return create_custom_oauth2_read_api(
            request,
            database_name,
            collection_name,
            skip=skip,
            limit=limit,
            return_keys=return_keys)

    # else
    raise Http404


def edit_simple_public_read_api(request, database_name, collection_name, slug):
    name = _("Edit Read API with No Authentication (Public)")
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


def edit_simple_ipauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    name = _("Edit Read API with IP-Based Authentication")
    ss = get_object_or_404(IPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = IPAuthReadAPIForm(request.POST, instance=ss)
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
               'form': IPAuthReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_simple_oauth2_read_api(
        request,
        database_name,
        collection_name,
        slug):
    name = _("Edit Read API with OAuth2 Authentication")
    ss = get_object_or_404(OAuth2ReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = OAuth2ReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save()
            messages.success(request, _("API saved."))
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
               'form': OAuth2ReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_custom_public_read_api(request, database_name, collection_name, slug):
    name = _("Edit Macro Read API with No Authentication (Public)")
    ss = get_object_or_404(CustomPublicReadAPI, database_name=database_name,
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
    name = _("Edit Macro Basic HTTP Authentication Read API")
    ss = get_object_or_404(CustomHTTPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = CustomHTTPAuthReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save(commit=False)
            ss.user = request.user
            ss.save()
            messages.success(
                request, _("API edited."))
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


def edit_custom_ipauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    print(database_name, collection_name, slug)
    name = _("Edit Macro Read API with IP-Based Authentication")
    ss = get_object_or_404(CustomIPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = CustomIPAuthReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save(commit=False)
            ss.user = request.user
            ss.save()
            messages.success(
                request, _("API updated."))
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
               'form': CustomIPAuthReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def edit_custom_oauth2_read_api(
        request,
        database_name,
        collection_name,
        slug):
    name = _("Edit Macro Read API with OAuth2 Authentication")
    ss = get_object_or_404(CustomOAuth2ReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)

    if request.method == 'POST':
        form = CustomOAuth2ReadAPIForm(request.POST, instance=ss)
        if form.is_valid():
            ss = form.save(commit=False)
            ss.user = request.user
            ss.save()
            messages.success(
                request, _("API updated."))
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
               'form': CustomOAuth2ReadAPIForm(instance=ss)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


def delete_custom_public_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete CustomPublicReadAPI"""
    ss = get_object_or_404(CustomPublicReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_custom_httpauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete CustomHTTPAuthReadAPI"""
    ss = get_object_or_404(CustomHTTPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_custom_ipauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete CustomIPAuthReadAPI"""
    ss = get_object_or_404(CustomIPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_custom_oauth2_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete CustomOAuth2ReadAPI"""
    ss = get_object_or_404(CustomOAuth2ReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("API deleted."))
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
    messages.success(request, _("API deleted."))
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
    messages.success(request, _("API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_simple_ipauth_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete Simple IP Read API"""
    ss = get_object_or_404(IPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))


def delete_simple_oauth2_read_api(
        request,
        database_name,
        collection_name,
        slug):
    """Delete Simple PublicReadAPI"""
    ss = get_object_or_404(IPAuthReadAPI, database_name=database_name,
                           collection_name=collection_name, slug=slug)
    ss.delete()
    messages.success(request, _("API deleted."))
    return HttpResponseRedirect(
        reverse('djmongo_show_apis',
                args=(ss.database_name, ss.collection_name)))
