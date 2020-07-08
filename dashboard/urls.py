from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
	
	path('web-login', LoginView.as_view(), name = "web_login"),
	path('listener-users', ListenerUsers.as_view(), name = "listener_users"),
	path('admin-users', AdminUsers.as_view(), name = "admin_users"),
	path('artist-users', ArtistUsers.as_view(), name = "artist_users"),
	path('genre-list', GeneresList.as_view(), name = "genre_list"),
	path('info', UserInfo.as_view(), name = "info"),

]
