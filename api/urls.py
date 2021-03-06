"""music_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    # URL's same for both role
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('edit-profile', EditUserAPIView.as_view()),
    path('my-profile', UserInformation.as_view()),
    path('token-validate', ValidateToken.as_view()),





    # URL's related to artist
    path('album', AddAlbumAPIView.as_view()),





    # URL's related to listener
    path('artist-list', AllArtist.as_view()),
    path('artist-detail/<int:pk>', ArtistDetail.as_view()),
    path('like-artist', LikeArtistAPIView.as_view()),
    path('dislike-artist', DislikeArtist.as_view()),

    
    path('song-view', SongsAPIView.as_view()),
    path('get-songs', GetSongsAPIView.as_view()),
    path('album/<album_id>', AlbumDetail.as_view(),name="album_detail"),


    path('send-login-link', SendLoginLinkAPIView.as_view()),
    
    # path('user-add-song', UserAddSongAPIView.as_view()),
    # path('user-song-list', UserSongListAPIView.as_view()),

    path('songs-liked-artist', SongsOfLikedArtistAPIView.as_view()),
            

    path('like-song', LikeSongAPIView.as_view()),
    path('hide-song', HideSongAPIView.as_view()),
    path('hidden-artist', HideArtistApi.as_view()),

    path('hidden-artist-song', SongsOfHiddenArtist.as_view()),


    path('create-playlist', CreatePlaylistAPIView.as_view()),
    path('song-to-playlist', PlaylistTrackAPIView.as_view()),
    path('create-playlist/<int:playlist_id>', ListSongsByPlaylistAPIView.as_view()),

    path('user-list', UserList.as_view()),
    path('my-follower', MyFollowerList.as_view()),
    path('my-following', MyFollowingList.as_view()),
    path('country-list', CountryList.as_view()),
    path('genre-list', GenreList.as_view()),

    ## password update apis ###
    path('change-password', ChangePasswordApi.as_view()),
    path('forget-password', ForgetPasswordLinkAPIView.as_view()),
    path('reset-password', ResetPasswordAPIView.as_view()),


]
