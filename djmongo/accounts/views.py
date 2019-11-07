#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import (LoginForm, UserCreationForm, UserUpdateForm,
                    APIUserUpdateForm, APIUserCreationForm)
from .decorators import json_login_required, access_required
from .models import SocialGraph
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User


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
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    next = request.GET.get('next', '')
                    if next:
                        # If a next is in the URL, then go there
                        return HttpResponseRedirect(next)
                    # otherwise just go to home.
                    return HttpResponseRedirect(reverse('djmongo_show_dbs'))
                else:
                    # The user exists but is_active=False
                    messages.error(
                        request, _("""Your account is inactive
                                   so you may not log in."""))

                    return render(request, 'djmongo/console/login2.html',
                                  {'form': form})
            else:
                messages.error(request, _("Invalid username or password."))

                return render(request, 'djmongo/console/login2.html',
                              {'form': form})

        else:
            return render(request,
                          'djmongo/console/login2.html',
                          {'form': form})
    # this is a GET
    return render(request, 'djmongo/console/login2.html',
                  {'form': LoginForm()})


@json_login_required
def api_test_credentials(request):
    message = _("Your API credentials for user %s are valid.") \
        % (request.user)
    jsonstr = {"code": 200, "message": message}
    jsonstr = json.dumps(jsonstr, indent=4,)
    return HttpResponse(jsonstr, status=200, content_type="application/json")


@json_login_required
@access_required("create-other-users")
def api_delete_user(request, email):
    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        message = "User %s does not exist." % (email)
        jsond = {"code": 404, "message": message}
        jsonstr = json.dumps(jsond, indent=4,)
        return HttpResponse(
            jsonstr,
            status=404,
            content_type="application/json")

    u.delete()
    message = "User %s deleted." % (email)
    jsond = {"code": 200, "message": message}
    jsonstr = json.dumps(jsond, indent=4,)
    return HttpResponse(jsonstr, status=200, content_type="application/json")


@login_required
def user_create(request):
    print(request.user)

    name = _("Create User Account")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            # The form is invalid
            messages.error(
                request, _("Please correct the errors in the form."))
            return render(request, 'generic/bootstrapform.html',
                          {'form': form, 'name': name})
    # this is a GET
    context = {'name': name,
               'form': UserCreationForm()
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


@login_required
@access_required("create-other-users")
def user_update(request):
    name = _("Update User Account")
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
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
               'form': UserUpdateForm(instance=request.user)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


@json_login_required
@access_required("create-other-users")
def api_read_user(request, email):

    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        message = _("User %s does not exist.") % (email)
        jsond = {"code": 404, "message": message}
        jsonstr = json.dumps(jsond, indent=4,)
        return HttpResponse(
            jsonstr,
            status=404,
            content_type="application/json")

    user = {"first_name": u.first_name, "last_name": u.last_name,
            "username": u.username, "email": email,
            "date_joined": str(u.date_joined)}
    jsond = {"code": 200, "user": user}
    jsonstr = json.dumps(jsond, indent=4,)
    return HttpResponse(jsonstr, status=200,
                        content_type="application/json")


@login_required
@access_required("create-other-users")
def user_password(request):
    name = _("Update Password")
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _("Password successfully updated."))
            return HttpResponseRedirect(reverse('home'))
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
               'form': SetPasswordForm(user=request.user)
               }
    return render(request, 'djmongo/console/generic/bootstrapform.html',
                  context)


@json_login_required
@csrf_exempt
@access_required("create-other-users")
def api_user_create(request):
    name = _("API Create User Account")
    if request.method == 'POST':
        form = APIUserCreationForm(request.POST)
        if form.is_valid():
            result = form.save()
            # our new user was created so lets go ahead and
            # create a social graph between the creator and the new user
            grantor = User.objects.get(username=result['user']['username'])
            SocialGraph.objects.create(grantor=grantor, grantee=request.user)
            SocialGraph.objects.create(grantor=grantor, grantee=grantor)
            jsonstr = result
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(
                jsonstr,
                status=200,
                content_type="application/json")
        else:
            # the form had errors
            errors = []
            for nferror in form.non_field_errors():
                errors.append({'non_field': nferror})
            for k, v in form._errors.items():
                error = {'field': k, 'description': v}
                errors.append(error)
            jsonstr = {"code": 400,
                       "message": _("User creation failed due to errors."),
                       "errors": errors}
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(
                jsonstr,
                status=400,
                content_type="application/json")
    # this is an HTTP GET
    return render(request, 'djmongo/accounts/create.html',
                  {'name': name, 'form': APIUserCreationForm()})


@json_login_required
@csrf_exempt
@access_required("create-other-users")
def api_user_update(request):
    name = _("API Update User Account")
    if request.method == 'POST':

        if 'email' not in request.POST:
            jsonstr = {
                "code": 400,
                "message": _("Update did not identify the user by email."),
                "errors": [
                    _("Update did not identify the user by email."),
                ]}
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(
                jsonstr,
                status=400,
                content_type="application/json")

        try:
            user = User.objects.get(email=request.POST['email'])
        except:

            msg = _("User %s not found. Did you mean to perform a create?")\
                % (request.POST['email'])
            jsonstr = {"code": 404,
                       "message": "User not found.",
                       "errors": [msg, ]}
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(
                jsonstr,
                status=400,
                content_type="application/json")

        form = APIUserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            result = form.save()
            jsonstr = result
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(
                jsonstr,
                status=200,
                content_type="application/json")
        else:
            # the form had errors # CHECK
            errors = []
            if form.non_field_errors():
                for nferror in form.non_field_errors():
                    errors.append({'non_field': nferror})

            for k, v in form._errors.items():
                error = {'field': k, 'description': v}
                errors.append(error)
            jsonstr = {"code": 400,
                       "message": _("User update failed due to errors."),
                       "errors": errors}
            jsonstr = json.dumps(jsonstr, indent=4,)
            return HttpResponse(
                jsonstr,
                status=400,
                content_type="application/json")
    # this is an HTTP GET
    return render(request, 'djmongo/accounts/create.html',
                  {'name': name, 'form': APIUserUpdateForm()})
