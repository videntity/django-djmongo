#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_("Password"))
    required_css_class = 'required'


class UserCreationForm(forms.ModelForm):
    """
A form that creates a user, with no privileges, from the given username and
password.
"""
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and "
            "@/./+/-/_ only."),
        error_messages={
            'invalid': _(
                "This value may contain only letters, numbers and "
                "@/./+/-/_ characters.")})

    email = forms.EmailField(label=_("Email"))

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User = get_user_model()
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User = get_user_model()
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
A form that creates a user, with no privileges, from the given username and
password.
"""
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and "
            "@/./+/-/_ only."),
        error_messages={
            'invalid': _(
                "This value may contain only letters, numbers and "
                "@/./+/-/_ characters.")})

    email = forms.EmailField(label=_("Email"))

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class APIUserCreationForm(UserCreationForm):

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        userdict = {'username': str(user.username),
                    'email': str(user.email),
                    'first_name': str(user.first_name),
                    'last_name': str(user.last_name),
                    }

        result = {"code": 200,
                  "message": "User created successfully",
                  "user": userdict
                  }
        return result


class APIUserUpdateForm(UserUpdateForm):

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        userdict = {'username': str(user.username),
                    'email': str(user.email),
                    'first_name': str(user.first_name),
                    'last_name': str(user.last_name),
                    }

        result = {"code": 200,
                  "message": "User updated successfully",
                  "user": userdict
                  }
        return result
