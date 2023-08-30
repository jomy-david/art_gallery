from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home',views.home),
    path('administrator',views.admin),
    path('Login',views.login),
    path('artistAprovals',views.artistAp),
    path('register',views.register),
    
]