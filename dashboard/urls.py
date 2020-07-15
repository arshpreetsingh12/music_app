from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
	
	path('', HomePage.as_view(), name = "dashboard_home"),
	path('web-login', LoginView.as_view(), name = "web_login"),
	path('listener-users', ListenerUsers.as_view(), name = "listener_users"),
	path('admin-users', AdminUsers.as_view(), name = "admin_users"),
	path('artist-users', ArtistUsers.as_view(), name = "artist_users"),
	path('genre-list', GeneresList.as_view(), name = "genre_list"),
	path('info', UserInfo.as_view(), name = "info"),
	path('add-new-song', AddNewSongs.as_view(), name = "add_new_song"),
	path('add-new-playlist', AddNewPlaylist.as_view(), name = "add_new_playlist"),
	path('admin-profile', AdminProfile.as_view(), name = "admin_profile"),
	path('add-album', AddAlbum.as_view(), name = "add_album"),
	path('financial', Financial.as_view(), name = "financial"),
	path('add-admin', AddAdmin.as_view(), name = "add_admin"),
	path('all-playlist', AllPlayList.as_view(), name = "all_playlist"),
	path('promotions', PromostionView.as_view(), name = "promotions"),
	path('report-user', ReportUserView.as_view(), name = "report_user"),
	path('report', ReportView.as_view(), name = "report"),
	path('subscription', SubscriptionView.as_view(), name = "subscription"),
	path('add-genre', AddGenre.as_view(), name = "add_genre"),

]
