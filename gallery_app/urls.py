from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('administrator',views.admin),
    path('Login',views.login),
    path('artistAprovals',views.artistAp),
    
]