import binascii
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext




class HTTPAuthBackend(object):
    
    supports_object_permissions=False
    supports_anonymous_user=False
    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    


class BasicBackend:
    
    supports_object_permissions=False
    supports_anonymous_user=False
    
    def authenticate(self, username=None, password=None):
        #print "Basic backend", username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailBackend(BasicBackend):
    
    supports_object_permissions=False
    supports_anonymous_user=False
    
    def authenticate(self, username=None, password=None):
        
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        
        

class MobilePINBackend(BasicBackend):
    
    supports_object_permissions=False
    supports_anonymous_user=False
    
    def authenticate(self, username=None, password=None):    
        #We have a non-email address username we should try username
        try:
            user = User.objects.get(mobile_phone_number=username)
        except User.DoesNotExist:
            return None

        if str(user.pin)==str(password):
            return user
        else:
            return None