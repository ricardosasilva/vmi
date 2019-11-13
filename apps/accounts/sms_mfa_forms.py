from django import forms

from django.utils.translation import ugettext_lazy as _

# Copyright Videntity Systems Inc.


class MFACodeForm(forms.Form):
    code = forms.CharField(widget=forms.PasswordInput, max_length=30,
                           label=_('Code*'))
    required_css_class = 'required'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label=_('Username, email, or account number'),
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your username, email, or account number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), max_length=150,
                               label=_('Password'))
    required_css_class = 'required'

    def clean_username(self):
        return self.cleaned_data.get("username", "").strip().lower()
