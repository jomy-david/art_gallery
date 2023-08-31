from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home',views.home),
    path('Gallery',views.Gallery),
    path('administrator',views.admin),
    path('register',views.register),
    path('Login',views.login),
    path('logout',views.logout),
    path('artistAprovals',views.artistAp),
    path('aproveArtist',views.aproveArtist),
    path('denyArtist',views.denyArtist),
    path('viewArtist',views.viewArtist),
    path('editGallery',views.editGallery),
    path('artistHome',views.artistHome),
    path('artistEdit',views.editArtist),
    path('addPost',views.addPost),
    path('error',views.error),
    path('test',views.test),
    
]