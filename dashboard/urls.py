from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'dashboard'
urlpatterns = [

    path('purchase_courses', views.PurchaseCourses, name='purchase_courses'),  
    path('view_course/<int:ids>/', views.ViewCourse, name='view_course'),  
    path('make_payment/<int:id>/<int:amount>/', views.MakePayment, name='make_payment'),  
    path('bought_courses', views.BoughtCourses, name='bought_courses'),  
    path('handlerequest/<slug:username>/<int:id>/<slug:order_id>/<int:amount>/', views.handlerequest, name='handlerequest'),
    path('register_card', views.RegisterCard, name='register_card'),
    
]
