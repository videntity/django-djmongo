import sys, types, datetime, os, json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from forms import *
from decorators import json_login_required, access_required
from models import SocialGraph
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

def simple_logout(request):
    logout(request)
    messages.success(request, _("Logged out successfully."))
    return HttpResponseRedirect(reverse('login'))


def simple_email_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user=authenticate(email=email, password=password)
            next = request.GET.get('next','')
            if user is not None:

                if user.is_active:
                    login(request,user)
                    if next:
                        return HttpResponseRedirect(next)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request,
                         _("Your account is inactive so you may not log in."))
                    return render_to_response('djmongo/console/login.html',
                                             {'form': form},
                                             RequestContext(request))
            else:
                messages.error(request, _("Invalid username or password."))
                return render_to_response('djmongo/console/login.html',
                                    {'form': form},
                                    RequestContext(request))

        else:
            return render_to_response('djmongo/console/login.html',
                              RequestContext(request, {'form': form}))
    #this is a GET
    return render_to_response('djmongo/console/login.html',
                              {'form': LoginForm()},
                              context_instance = RequestContext(request))




@json_login_required
def api_test_credentials(request):
    message ="Your API credentials for user %s are valid." % (request.user)
    jsonstr={"code": 200, "message": message}
    jsonstr=json.dumps(jsonstr, indent = 4,)
    return HttpResponse(jsonstr, status=200, content_type="application/json")







@json_login_required
@access_required("create-other-users")
def api_delete_user(request, email):
    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        message ="User %s does not exist." % (email)
        jsond={"code": 404, "message": message}
        jsonstr=json.dumps(jsond, indent = 4,)
        return HttpResponse(jsonstr, status=404, content_type="application/json")
        
    u.delete()
    message ="User %s deleted." % (email)
    jsond={"code": 200, "message": message}
    jsonstr=json.dumps(jsond, indent = 4,)
    return HttpResponse(jsonstr, status=200, content_type="application/json")
    
    

#@login_required
#@access_required("create-other-users")
@login_required
def user_create(request):
    print request.user
    
    name = _("Create User Account")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            #The form is invalid
            messages.error(request,_("Please correct the errors in the form."))
            return render_to_response('generic/bootstrapform.html',
                                           {'form': form,
                                            'name':name,
                                            },
                                           RequestContext(request))
    #this is a GET
    context= {'name':name,
              'form': UserCreationForm()
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))




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
            #The form is invalid
            messages.error(request,_("Please correct the errors in the form."))
            return render_to_response('djmongo/console/generic/bootstrapform.html',
                                           {'form': form,
                                            'name':name,
                                            },
                                           RequestContext(request))
   #this is a GET
    context= {'name':name,
              'form': UserUpdateForm(instance=request.user)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))




@json_login_required
@access_required("create-other-users")
def api_read_user(request, email):
    
    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        message ="User %s does not exist." % (email)
        jsond={"code": 404, "message": message}
        jsonstr=json.dumps(jsond, indent = 4,)
        return HttpResponse(jsonstr, status=404, content_type="application/json")
        
    user = {"first_name": u.first_name, "last_name":u.last_name,
            "username": u.username, "email": email,
            "date_joined": str(u.date_joined)}
    jsond={"code": 200, "user": user}
    jsonstr=json.dumps(jsond, indent = 4,)
    return HttpResponse(jsonstr, status=200, content_type="application/json")





@login_required
@access_required("create-other-users")
def user_password(request):
    name = _("Update Password")
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,_("Password successfully updated."))
            return HttpResponseRedirect(reverse('home'))
        else:
            #The form is invalid
            messages.error(request,_("Please correct the errors in the form."))
            return render_to_response('djmongo/console/generic/bootstrapform.html',
                                           {'form': form,
                                            'name':name,
                                            },
                                           RequestContext(request))

  #this is a GET

    context= {'name':name,
              'form': SetPasswordForm(user=request.user)
              }
    return render_to_response('djmongo/console/generic/bootstrapform.html',
                              RequestContext(request, context,))






@json_login_required
@csrf_exempt
@access_required("create-other-users")
def api_user_create(request):
    name = _("API Create User Account")
    if request.method == 'POST':
        form = APIUserCreationForm(request.POST)
        if form.is_valid():
            result=form.save()
            # our new user was created so lets go ahead and create a social graph
            # between the creator and the new user
            grantor=User.objects.get(username=result['user']['username'])
            s=SocialGraph.objects.create(grantor=grantor, grantee=request.user)
            try:
                s=SocialGraph.objects.create(grantor=grantor, grantee=grantor)
            except:
                pass
            jsonstr=result
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, status=200, content_type="application/json")
        else:
            # the form had errors
            errors=[]
            if form.non_field_errors():
                global_error={'global':global_error}
                errors.append()

            for k,v in form._errors.items():
                error={'field': k, 'description':v}
                errors.append(error)
            jsonstr={"code": 400,
                      "message": "User creation failed due to errors.",
                         "errors": errors}
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, status=400, content_type="application/json")
    # this is an HTTP GET
    return render_to_response('djmongo/accounts/create.html',
                    {'name':name, 'form': APIUserCreationForm(),},
                    RequestContext(request))
    









@json_login_required
@csrf_exempt
@access_required("create-other-users")
def api_user_update(request):
    name = _("API Update User Account")
    if request.method == 'POST':
        
        if not request.POST.has_key('email'):
            jsonstr = { "code": 400,
                        "message": "Update did not identify the user by email.",
                        "errors": ["Update did not identify the user by email.", ]}
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, status=400, content_type="application/json")
        
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            
            msg = "User %s not found.  Did you mean to perform a create?" % (request.POST['email'])
            jsonstr = { "code": 404,
                        "message": "User not found.",
                        "errors": [msg, ]}
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, status=400, content_type="application/json")
        
        form = APIUserUpdateForm(request.POST, instance=user)
        
        
        if form.is_valid():
            result=form.save()
            jsonstr=result
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, status=200, content_type="application/json")
        else:
            # the form had errors
            errors=[]
            if form.non_field_errors():
                global_error={'global':global_error}
                errors.append()

            for k,v in form._errors.items():
                error={'field': k, 'description':v}
                errors.append(error)
            jsonstr = { "code": 400,
                        "message": "User update failed due to errors.",
                        "errors": errors}
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, status=400, content_type="application/json")
    # this is an HTTP GET
    return render_to_response('djmongo/accounts/create.html',
                    {'name':name, 'form': APIUserUpdateForm(),},
                    RequestContext(request))

