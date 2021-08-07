from random import choice
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib import auth
from accounts.models import User
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class RegisterCardForm(forms.Form):
    
    CARD_CHOICES = [('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')]
    name_on_card =  forms.CharField(max_length= 40) 
    card_bank =  forms.CharField(max_length= 40) 
    card_number =  forms.CharField(max_length= 40) 
    expiry_month =  forms.CharField(max_length= 40)
    expiry_year =  forms.CharField(max_length= 40)
    card_type = forms.CharField(widget=forms.Select(choices=CARD_CHOICES), max_length='20', required=True)
    otp = forms.IntegerField()
