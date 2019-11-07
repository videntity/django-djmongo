#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render, get_object_or_404
import json
import sys
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from ..decorators import (kickout_400, kickout_404, kickout_500)
from django.http import HttpResponse, HttpResponseRedirect
from collections import OrderedDict
from ..mongoutils import write_mongo
from jsonschema import validate
from django.core.urlresolvers import reverse
from jsonschema.exceptions import ValidationError
from .models import WriteAPIOAuth2
from .forms import WriteAPIOAuth2Form, WriteAPIOAuth2DeleteForm
from django.utils.translation import ugettext_lazy as _
from .views import write_to_collection

@csrf_exempt
def write_to_collection_oauth2(request, slug):
    return write_to_collection(request, slug, WriteAPIOAuth2)    
