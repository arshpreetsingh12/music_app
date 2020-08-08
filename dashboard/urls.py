from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
	
	########## basic urls ########
	path('home/', HomePage.as_view(), name = "dashboard_home"),
	path('web-login/', LoginView.as_view(), name = "web_login"),
	path('logout/', Logout.as_view(), name = "logout"),
	

	########## admin related urls  ########
	path('admin-users/', AdminUsers.as_view(), name = "admin_users"),
	path('admin-profile/', AdminProfile.as_view(), name = "admin_profile"),
	path('add-admin/', AddAdmin.as_view(), name = "add_admin"),
	path('edit-admin/<int:user_id>/', EditAdmin.as_view(), name = "edit_admin"),


	########## all artists  ########
	path('artist-users/', ArtistUsers.as_view(), name = "artist_users"),
	
	########## all listener  ########
	path('listener-users/', ListenerUsers.as_view(), name = "listener_users"),

	########## Genre related urls  ########
	path('genre-list/', GeneresList.as_view(), name = "genre_list"),
	path('add-genre/', AddGeneres.as_view(), name = "add_genre"),
	path('edit-genre/<int:genre_id>/', EditGeneres.as_view(), name = "edit_genre"),
	

	########## logged in user's profile  ########
	path('my-profile/', MyProfile.as_view(), name = "my_profile"),
	
	########## songs related urls  ########
	path('all-songs/', AllSongs.as_view(), name = "all_songs"),
	path('add-new-song/', AddNewSongs.as_view(), name = "add_new_song"),
	path('edit-song/<int:song_id>/', EditSongs.as_view(), name = "edit_song"),
	

	########## albums related urls  ########
	path('all-albums/', AllAlbums.as_view(), name = "all_albums"),
	path('add-album/', AddAlbum.as_view(), name = "add_album"),
	path('view-album/', ViewAlbum.as_view(), name = "view_album"),
	path('edit-album/<int:album_id>/', EditAlbum.as_view(), name = "edit_album"),
	

	########## playlist related urls  ########
	path('all-playlist/', AllPlayList.as_view(), name = "all_playlist"),
	path('add-new-playlist/', AddNewPlaylist.as_view(), name = "add_new_playlist"),
	path('edit-playlist/<int:playlist_id>/', EditPlayList.as_view(), name = "edit_playlist"),
	path('delete-playlist/', DeletePlaylist.as_view(), name = "delete_playlist"),


	########## other urls  ############
	path('financial/', Financial.as_view(), name = "financial"),
	path('promotions/', PromostionView.as_view(), name = "promotions"),
	
	path('report-user/', ReportUserView.as_view(), name = "report_user"),
	path('report/', ReportView.as_view(), name = "report"),
	
	path('subscription/', SubscriptionView.as_view(), name = "subscription"),
	

]
