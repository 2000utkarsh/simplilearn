from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [

    path('singup', views.SignUp, name='signup'),   

]
