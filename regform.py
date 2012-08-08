#---------------------------regform.py----------------------------------
#This python file contains form classes. This allows an html form to be
#defined using the django.forms library. The main benefits of using this 
#library is that the form validation can be handled by it.
#The two password field contain 'widget=forms.PasswordInput', in html
#this is '<input type="password" name"password" />.
#-----------------------------------------------------------------------
from django import forms

#Create class for registeration form
class regForm(forms.Form):
    firstName = forms.CharField(required=True)
    lastName = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm = forms.CharField(widget=forms.PasswordInput, required=True)
