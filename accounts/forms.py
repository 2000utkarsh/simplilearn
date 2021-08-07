from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib import auth
from accounts.models import User
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class SignUpForm(UserCreationForm):
    
    class Meta():
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        model = User

        def __init__(self, *args, **kwargs):
            super.__init__(*args, **kwargs)
            self.fields['username'].label = 'Username'
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['email'].label = 'Email'

            self.fields['first_name'].widget.attrs.update({'class' : 'input'})
            self.fields['last_name'].widget.attrs.update({'class' : 'input'})
            self.fields['username'].widget.attrs.update({'class' : 'input'})
            self.fields['email'].widget.attrs.update({'class' : 'input'})
            self.fields['password1'].widget.attrs.update({'class' : 'input'})
            self.fields['password2'].widget.attrs.update({'class' : 'input'})
            self.fields['user_choice'].widget.attrs.update({'class' : 'input'})


