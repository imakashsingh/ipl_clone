from django import forms

from myapp.models import *

class Login_form(forms.Form):
    class Meta:
        fields = '__all__'
        widgets = {
            'username' : forms.TextInput(),
            'password' : forms.PasswordInput(),
        }

class SignUp_form(forms.Form):
    class Meta:
        widgets = {
            'first_name' : forms.TextInput(),
            'last_name' : forms.TextInput(),
            'username' : forms.TextInput(),
            'password' : forms.PasswordInput(),
        }