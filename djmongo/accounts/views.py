#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from .forms import LoginForm
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages


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

