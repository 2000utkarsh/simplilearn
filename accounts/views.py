from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from . import forms
from .import models
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from accounts.models import User
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def SignUp(request):

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']


            user = authenticate(username=username, password = password)
            return render(request, 'success.html', {'success': 'User Created Successfully','response': 'signup_success'})
    else:
        form = forms.SignUpForm()
         
        return render(request, 'signup.html', {'form':form})
