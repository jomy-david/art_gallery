from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home',views.home),
    path('administrator',views.admin),
    path('Login',views.login),
    path('logout',views.logout),
    path('artistAprovals',views.artistAp),
    path('viewArtist',views.viewArtist),
    path('register',views.register),
    path('error',views.error),
    path('test',views.test),
    
]