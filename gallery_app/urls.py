from django.urls import path
from . import views

urlpatterns=[
    # Main
    path('',views.home),
    path('home',views.home),
    path('Gallery',views.Gallery),
    path('viewPost',views.post),
    path('likePost',views.likePost),
    path('addComment',views.addComment),
    # Admin
    path('administrator',views.admin),
    path('register',views.register),
    path('Login',views.login),
    path('logout',views.logout),
    path('artistAprovals',views.artistAp),
    path('aproveArtist',views.aproveArtist),
    path('denyArtist',views.denyArtist),
    path('viewArtist',views.viewArtist),
    path('postAprovals',views.postAp),
    path('aprovePost',views.aprovePost),
    path('denyPost',views.denyPost),
    path('editGallery',views.editGallery),
    path('delCat',views.delCat),
    # Artist
    path('artistHome',views.artistHome),
    path('artistEdit',views.editArtist),
    path('ArtistPage',views.artistProfile),
    path('addPost',views.addPost),
    # User
    path('userHome',views.userHome),
    # Others
    path('error',views.error),
    path('test',views.test),

    
]