#imports
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from api.models import *
from django.db.models import Q
from django.urls import reverse
from datetime import datetime,date,timedelta
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


"""  Dashboard Home page   """
class HomePage(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'dashbaord.html'

	def get(self,request):
		dashboard_active = "active"
		today = datetime.today()
		week_start_date = today.date() - timedelta(days = 7)
		weekly_listener = UserDetail.objects.filter(is_listener = True, created_at__date__gte = week_start_date).count()
		monthly_start_date = today.date() - timedelta(days = 30)
		monthly_listener = UserDetail.objects.filter(is_listener = True, created_at__date__gte = monthly_start_date).count()
		daily_listener = UserDetail.objects.filter(is_listener = True, created_at__date__gte = today.date()).count()
		return render(request,self.template_name,locals())

""" 
	This view for user login  
								"""
class LoginView(View):
	template_name = "login.html"

	def get(self,request):
		return render(request,self.template_name,locals())

	def post(self, request, *args, **kwargs):
		email = request.POST.get('email').lower()
		password = request.POST.get('password')
		try:
			if email != "" and password != "": 
				user= User.objects.get(Q(email = email)|Q(username = email))

				if user.is_active == True:
					userauth = authenticate(username=user.username, password=password)
					if userauth:
						login(request, user,backend='django.contrib.auth.backends.ModelBackend')
						user_info = UserDetail.objects.filter(user = user).last()
						if user_info:
							if user_info.is_artist:
								return HttpResponseRedirect(reverse('my_profile'))
							else:
								return HttpResponseRedirect(reverse('artist_users'))
						if user.is_staff or user.is_superuser:
							return HttpResponseRedirect(reverse('dashboard_home'))
							
					else:
						messages.error(request,'Invalid credentials.')
						return HttpResponseRedirect(reverse('web_login'))
				else:
					messages.error(request,'Your account is not verify.')
					return HttpResponseRedirect(reverse('web_login'))
			else:
				messages.error(request,'Incorrect email and password.')
				return HttpResponseRedirect(reverse('web_login'))

		except Exception as e:
			print(str(e))
			messages.info(request,'No such account exist.')
			return HttpResponseRedirect(reverse('web_login'))


""" 
	This view for user logout  
								"""
class Logout(View):

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect(reverse('web_login'))


"""  Logged in user's profile   """
class MyProfile(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'my-profile.html'

	def get(self,request):
		user = User.objects.get(id = request.user.id)
		user_info = UserDetail.objects.filter(user = request.user).last()
		return render(request,self.template_name,locals())

	def post(self,request):
		response = {}
		username = request.POST.get('username')
		email = request.POST.get('email')
		if username and email:
			user = User.objects.get(pk = request.user.id)
			user.username = username 
			user.email = email
			user.save()
			response['status'] = True
		else:
			response['status'] = False
		return HttpResponse(json.dumps(response),content_type="application/json")


""" 
	listener user list 
							"""
class ListenerUsers(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'listener_users.html'

	def get(self,request):
		listener_active = "active"
		users = UserDetail.objects.filter(is_listener = True, is_deleted = False)

		row = request.GET.get('row', 5)
		page = request.GET.get('page', 1)
		paginator = Paginator(users, row)
		try:
			page_data = paginator.page(page)
		except PageNotAnInteger:
			page_data = paginator.page(1)
		except EmptyPage:
			page_data = paginator.page(paginator.num_pages)
		return render(request,self.template_name,locals())


	####### delete ListenerUsers ###############	
	def post(self,request):
		response = {}
		user_id = request.POST.get('user_id')

		try:
			user_obj = UserDetail.objects.get(pk = user_id)
			user_obj.is_deleted = True
			user_obj.user.is_active = False
			user_obj.user.save()
			user_obj.save()
			response['status'] = True
		except Exception as e:
			response['status'] = False
		return HttpResponse(json.dumps(response),content_type="application/json")

""" 
	Artist user list 
					  """
class ArtistUsers(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'artist_users.html'

	def get(self,request):
		artist_active = "active"
		users = UserDetail.objects.filter(is_artist = True, is_deleted = False)

		row = request.GET.get('row', 5)
		page = request.GET.get('page', 1)
		paginator = Paginator(users, row)
		try:
			page_data = paginator.page(page)
		except PageNotAnInteger:
			page_data = paginator.page(1)
		except EmptyPage:
			page_data = paginator.page(paginator.num_pages)
		return render(request,self.template_name,locals())


	####### delete artist ###############	
	def post(self,request):
		response = {}
		user_id = request.POST.get('user_id')

		try:
			user_obj = UserDetail.objects.get(pk = user_id)
			user_obj.is_deleted = True
			user_obj.user.is_active = False
			user_obj.user.save()
			user_obj.save()
			response['status'] = True
		except Exception as e:
			response['status'] = False
		return HttpResponse(json.dumps(response),content_type="application/json")



""" 
	Admin user list 
					  """
class AdminUsers(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'admin-users.html'

	def get(self,request):
		admin_active = "active"
		users = User.objects.filter(is_staff = True).exclude(pk = request.user.id)

		row = request.GET.get('row', 5)
		page = request.GET.get('page', 1)
		paginator = Paginator(users, row)
		try:
			page_data = paginator.page(page)
		except PageNotAnInteger:
			page_data = paginator.page(1)
		except EmptyPage:
			page_data = paginator.page(paginator.num_pages)
		return render(request,self.template_name,locals())



	####### delete admin ###############	
	def post(self,request):
		response = {}
		user_id = request.POST.get('user_id')

		try:
			user_obj = User.objects.get(pk = user_id)
			user_obj.is_active = False
			user_obj.save()
			response['status'] = True
		except Exception as e:
			response['status'] = False
		return HttpResponse(json.dumps(response),content_type="application/json")



""" Admin profile """
class AdminProfile(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'admin-profile.html'

	def get(self,request):
		return render(request,self.template_name,locals())
	

""" Add New Admin """
class AddAdmin(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'add-new-admin.html'

	def get(self,request):

		return render(request,self.template_name,locals())	

	def post(self,request):
		username = request.POST.get('user_name').lower()
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email').lower()
		status = request.POST.get('status')
		address = request.POST.get('address')
		phone_number = request.POST.get('phone')

		try:
			user = User.objects.get(Q(username = username)|Q(email = email))
			messages.info(request, "User already exist.")
			return HttpResponseRedirect(reverse('add_admin'))
		except User.DoesNotExist:
			add_user = User.objects.create(
				username = username,
				email = email,
				first_name = first_name,
				last_name = last_name
				)
			add_user.set_password(password)
			if status == "A":
				add_user.is_active = True
			else:
				add_user.is_active = False
			add_user.is_staff = True
			add_user.save()

			extra_detail = AdminDetail.objects.create(
				user = add_user,
				phone_number = phone_number,
				address = address
				)

			messages.success(request, "User successfully added.")
			return HttpResponseRedirect(reverse('admin_users'))


""" Edit  Admin """
class EditAdmin(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'edit-admin.html'

	def get(self,request, user_id):
		user = User.objects.get(pk = user_id)
		return render(request,self.template_name,locals())	

	def post(self,request,user_id):
		username = request.POST.get('user_name')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		status = request.POST.get('status')
		address = request.POST.get('address')
		phone_number = request.POST.get('phone')

		try:
			user = User.objects.get(pk = user_id)
			user.username = username
			user.email = email
			user.first_name = first_name
			if last_name:
				user.last_name = last_name

			if password:
				user.set_password(password)
			if status == "A":
				user.is_active = True
			else:
				user.is_active = False
			user.is_staff = True
			user.save()

			extra_detail,created = AdminDetail.objects.get_or_create(user = user)
			extra_detail.phone_number = phone_number
			extra_detail.address = address
			extra_detail.save()

			messages.success(request, "User successfully updated.")
			return HttpResponseRedirect(reverse('admin_users'))
		except User.DoesNotExist:
			messages.error(request, "Invalid user id.")
			return HttpResponseRedirect('/dashboard/edit-admin/' + str(user_id))

""" 
	 GenreList list 
					"""
class GeneresList(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'genre_list.html'

	def get(self,request):
		genre_active = "active"
		genre_list = Genre.objects.all()
		to_date = datetime.today().date()

		row = request.GET.get('row', 5)
		page = request.GET.get('page', 1)
		paginator = Paginator(genre_list, row)
		try:
			page_data = paginator.page(page)
		except PageNotAnInteger:
			page_data = paginator.page(1)
		except EmptyPage:
			page_data = paginator.page(paginator.num_pages)
		return render(request,self.template_name,locals())


	####### delete genre ###############	
	def post(self,request):
		response = {}
		genre_id = request.POST.get('genre_id')

		try:
			genre_obj = Genre.objects.get(pk = genre_id)
			genre_obj.is_deleted = True
			genre_obj.save()
			response['status'] = True
		except Exception as e:
			response['status'] = False
		return HttpResponse(json.dumps(response),content_type="application/json")
	


""" 
	Add Genre 
				"""
class AddGeneres(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'add-genre.html'

	def get(self,request):
		genre_active = "active"
		return render(request,self.template_name,locals())

	def post(self, request):
		genre_name = request.POST.get('genre_name')
		genre_status = request.POST.get('genre_status')

		try:
			add_genre = Genre.objects.create(
				genre = genre_name
				)
			if genre_status == "A":
				add_genre.status = True
			else:
				add_genre.status = False
			add_genre.save()
			messages.success(request, "Genre successfully added.")
			return HttpResponseRedirect(reverse('genre_list'))
		except Exception as e:
			messages.error(request, "Something went wrong.")
			return HttpResponseRedirect(reverse('add_genre'))



class EditGeneres(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'edit-genre.html'

	def get(self,request,genre_id):
		genre_active = "active"
		genre_data = Genre.objects.get(pk = genre_id)
		return render(request,self.template_name,locals())

	def post(self, request, genre_id):
		genre_name = request.POST.get('genre_name')
		genre_status = request.POST.get('genre_status')

		try:
			add_genre = Genre.objects.get(pk = genre_id)
			add_genre.genre = genre_name
			if genre_status == "A":
				add_genre.status = True
			else:
				add_genre.status = False
			add_genre.save()
			messages.success(request, "Genre successfully updated.")
			return HttpResponseRedirect(reverse('genre_list'))
		except Exception as e:
			messages.error(request, "Something went wrong.")
			return HttpResponseRedirect('/dashboard/edit-genre/' + str(genre_id))


""" All songs List """
class AllSongs(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'all-songs.html'

	def get(self,request):
		all_song = ''
		try:
			if request.user.is_superuser or request.user.is_staff:
				all_song = Song.objects.all()
			else:
				user = UserDetail.objects.get(user_id = request.user.id)
				if user.is_artist:
					all_song = Song.objects.filter(user = user)
				else:
					all_song = Song.objects.all()
		except Exception as e:
			pass
		
		song_active = "active"
		to_date = datetime.today().date()
		row = request.GET.get('row', 5)
		page = request.GET.get('page', 1)
		paginator = Paginator(all_song, row)
		try:
			page_data = paginator.page(page)
		except PageNotAnInteger:
			page_data = paginator.page(1)
		except EmptyPage:
			page_data = paginator.page(paginator.num_pages)
		return render(request,self.template_name,locals())


	####### delete song ###############	
	def post(self,request):
		response = {}
		song_id = request.POST.get('song_id')

		try:
			song_obj = Song.objects.get(pk = song_id)
			song_obj.delete = True
			song_obj.save()
			response['status'] = True
		except Exception as e:
			response['status'] = False
		return HttpResponse(json.dumps(response),content_type="application/json")

""" Add New Songs """
class AddNewSongs(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'add-new-songs.html'

	def get(self,request):
		song_active = "active"
		all_artist = UserDetail.objects.filter(is_artist = True)
		return render(request,self.template_name,locals())

	def post(self, request):
		artist = request.POST.get('artist')
		song_title = request.POST.get('song_title')
		song_length = request.POST.get('song_length')
		song_img = request.FILES.get('song_img')
		song_mp3 = request.FILES.get('song_mp3')
		description = request.POST.get('description')

		try:
			add_song = Song.objects.create(
				user_id = artist,
				song_title = song_title
				)
			if song_length:
				add_song.song_length = song_length		
			if song_img:
				add_song.song_image = song_img
			if song_mp3:
				add_song.song_mp3 = song_mp3
			if description:
				add_song.description = description
			add_song.save()
			messages.success(request, "Song successfully added.")
		
		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong.")
		return HttpResponseRedirect(reverse('add_new_song'))

""" Edit Songs """
class EditSongs(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'edit-song.html'

	def get(self,request,song_id):
		song_active = "active"
		all_artist = UserDetail.objects.filter(is_artist = True)
		song = Song.objects.get(pk = song_id)
		return render(request,self.template_name,locals())

	def post(self, request,song_id):
		artist = request.POST.get('artist')
		song_title = request.POST.get('song_title')
		song_length = request.POST.get('song_length')
		song_img = request.FILES.get('song_img')
		song_mp3 = request.FILES.get('song_mp3')
		description = request.POST.get('description')

		try:
			add_song = Song.objects.get(pk = song_id)
			if artist:
				add_song.user_id = artist
			if song_title:
				add_song.song_title = song_title
			if song_length:
				add_song.song_length = song_length		
			if song_img:
				add_song.song_image = song_img
			if song_mp3:
				add_song.song_mp3 = song_mp3
			if description:
				add_song.description = description
			add_song.save()
			messages.success(request, "Song successfully updated.")
			return HttpResponseRedirect(reverse('all_songs'))
		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong.")
			return HttpResponseRedirect('dashboard/edit-song/' + str(song_id))




""" All Album's list """
class AllAlbums(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'all-albums.html'

	def get(self,request):
		try:
			if request.user.is_superuser or request.user.is_staff:
				all_albums = Album.objects.all()
			else:
				user = UserDetail.objects.get(user_id = request.user.id)
				if user.is_artist:
					all_albums = Album.objects.filter(artist = user)
				else:
					all_albums = Album.objects.all()
		except Exception as e:
			pass
		return render(request,self.template_name,locals())	


""" Add New Album """
class AddAlbum(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'add-album.html'

	def get(self,request):
		album_active = "active"
		all_artist = UserDetail.objects.filter(is_artist = True)
		if request.user.is_superuser or request.user.is_staff:
			songs = Song.objects.filter(delete = False)
		else:
			current_user = UserDetail.objects.get(user_id = request.user.id)
			songs = Song.objects.filter(user = current_user, delete = False)
		return render(request,self.template_name,locals())

	def post(self, request):
		artist = request.POST.get('artist')
		twitter_url = request.POST.get('twitter_url')
		album_length = request.POST.get('album_length')
		google_url = request.POST.get('google_url')
		website_url = request.POST.get('website_url')
		description = request.POST.get('description')
		fb_url = request.POST.get('fb_url')
		album_title = request.POST.get('album_title')
		album_pic = request.FILES.get('album_pic')
		selected_song = request.POST.getlist('selected_song')

		try:
			add_album = Album.objects.create(
				artist_id = artist,
				album = album_title,
				)
			add_album.song.set(selected_song)
			if album_pic:
				add_album.album_pic = album_pic
			
			if fb_url:
				add_album.fb_url = fb_url
			if twitter_url:
				add_album.twitter_url = twitter_url
			if google_url:
				add_album.google_url = google_url
			if website_url:
				add_album.website_url = website_url
			if description:
				add_album.description = description
			if album_length:
				add_album.album_length = album_length
			
			add_album.save()
			messages.success(request, "Album successfully added.")
			return HttpResponseRedirect(reverse('all_albums'))
		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong.")
			return HttpResponseRedirect(reverse('add_album'))


""" View album """
class ViewAlbum(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'view-album.html'

	def get(self,request,album_id):
		album = Album.objects.filter(pk = album_id).last()
		all_artist = UserDetail.objects.filter(is_artist = True)
		songs = Song.objects.all()
		return render(request,self.template_name,locals())

""" Edit Album """
class EditAlbum(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'edit-album.html'

	def get(self,request,album_id):
		try:
			album = Album.objects.get(pk = album_id)
			all_artist = UserDetail.objects.filter(is_artist = True)
			if request.user.is_superuser or request.user.is_staff:
				songs = Song.objects.all()
			else:
				current_user = UserDetail.objects.get(user_id = request.user.id)
				songs = Song.objects.filter(user = current_user)
		except Exception as e:
			pass		
		return render(request,self.template_name,locals())

	def post(self, request, album_id):
		artist = request.POST.get('artist')
		twitter_url = request.POST.get('twitter_url')
		album_length = request.POST.get('album_length')
		google_url = request.POST.get('google_url')
		website_url = request.POST.get('website_url')
		description = request.POST.get('description')
		fb_url = request.POST.get('fb_url')
		album_title = request.POST.get('album_title')
		album_pic = request.FILES.get('album_pic')
		selected_song = request.POST.getlist('selected_song')

		try:
			add_album = Album.objects.get(pk = album_id)
			add_album.song.set(selected_song)
			
			if artist:
				add_album.artist_id = artist
		
			if album_title:
				add_album.album = album_title 
		
			if album_pic:
				add_album.album_pic = album_pic
			
			if fb_url:
				add_album.fb_url = fb_url
		
			if twitter_url:
				add_album.twitter_url = twitter_url
		
			if google_url:
				add_album.google_url = google_url
		
			if website_url:
				add_album.website_url = website_url
			
			if description:
				add_album.description = description
			
			if album_length:
				add_album.album_length = album_length
			
			add_album.save()
			messages.success(request, "Album successfully updated.")
			return HttpResponseRedirect(reverse('all_albums'))

		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong.")
			return HttpResponseRedirect('/dashboard/edit-album/' + str(album_id))


""" Financial """
class Financial(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'finacial.html'

	def get(self,request):
		return render(request,self.template_name,locals())	


""" Add New Playlist """
class AddNewPlaylist(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'add-playlist.html'

	def get(self,request):
		playlist_active = "active"
		artist_user = UserDetail.objects.filter(is_artist = True)
		songs = Song.objects.all()
		return render(request,self.template_name,locals())

	def post(self,request):
		title = request.POST.get('title')
		artist = request.POST.get('artist')
		cover_img = request.FILES.get('cover_img')
		discription = request.POST.get('discription')
		selected_song = request.POST.getlist('selected_song')
		playlist_length = request.POST.get('album_length')

		try:
			artist_info = ArtistInfo.objects.get(info_id = artist)
			add_play_list = Playlist.objects.create(
				user = request.user,
				artist = artist_info,
				playlist = title,
				description = discription   
				)
			if cover_img:
				add_play_list.cover_image = cover_img
			if playlist_length:
				add_play_list.Playlist_length = playlist_length
			add_play_list.save()
			for song in selected_song:
				PlaylistTrack.objects.create(
					user = request.user,
					playlist = add_play_list,
					song_id = song
					)
			messages.info(request, "Playlist successfully added.")
			return HttpResponseRedirect(reverse('all_playlist'))
		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong.Please try again.")
			return HttpResponseRedirect(reverse('add_new_playlist'))



""" Add New Playlist """
class AllPlayList(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'playlist.html'

	def get(self,request):
		playlist_active = "active"
		playlists = Playlist.objects.all()
		return render(request,self.template_name,locals())


""" Edit Playlist """
class EditPlayList(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'edit-playlist.html'

	def get(self,request,playlist_id):
		playlist_active = "active"
		playlist_data = Playlist.objects.get(pk = playlist_id)
		artist_user = UserDetail.objects.filter(is_artist = True)
		songs = Song.objects.all()
		return render(request,self.template_name,locals())

	def post(self,request,playlist_id):
		title = request.POST.get('title')
		artist = request.POST.get('artist')
		cover_img = request.FILES.get('cover_img')
		discription = request.POST.get('discription')
		selected_song = request.POST.getlist('selected_song')
		playlist_length = request.POST.get('album_length')

		try:
			artist_info = ArtistInfo.objects.get(info_id = artist)
			edit_play_list = Playlist.objects.get(pk = playlist_id)

			if title:
				edit_play_list.playlist = title
			
			if artist:
				edit_play_list.artist = artist_info
			
			if discription:
				edit_play_list.discription = discription

			if playlist_length:
				edit_play_list.Playlist_length = playlist_length

			if cover_img:
				edit_play_list.cover_image = cover_img
			
			edit_play_list.save()

			############## delete all playlist songs ###############
			PlaylistTrack.objects.filter(playlist = edit_play_list).delete()

			############## add playlist songs ###############
			for song in selected_song:
				PlaylistTrack.objects.create(
					user = request.user,
					playlist = edit_play_list,
					song_id = song
					)
			messages.info(request, "Playlist successfully updated.")
			return HttpResponseRedirect(reverse('all_playlist'))
		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong. Please try again.")
			return HttpResponseRedirect('/dashboard/edit-playlist/' + str(playlist_id))



""" Add New Playlist """
class PromostionView(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'promostion.html'

	def get(self,request):
		promo_active = "active"
		return render(request,self.template_name,locals())

		
""" Add New Playlist """
class ReportUserView(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'report-user.html'

	def get(self,request):
		report_active = "active"
		return render(request,self.template_name,locals())

""" Add New Playlist """
class ReportView(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'report.html'

	def get(self,request):
		return render(request,self.template_name,locals())


""" Add New Playlist """
class SubscriptionView(LoginRequiredMixin,View):
	login_url = 'web_login'
	template_name = 'subscrption-offers.html'

	def get(self,request):
		return render(request,self.template_name,locals())


