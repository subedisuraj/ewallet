__author__ = 'Dell'

from django import forms

class Bank_registration_form(forms.Form):
    account_no = forms.CharField()
    pin_no = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
#    password = forms.PasswordInput()
    confirm_password = forms.CharField(widget=forms.PasswordInput())



