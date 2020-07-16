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

class HomePage(View):
	template_name = 'dashbaord.html'

	def get(self,request):
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
		email = request.POST.get('email')
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
								return HttpResponseRedirect(reverse('info'))
							else:
								return HttpResponseRedirect(reverse('artist_users'))
						if user.is_staff or user.is_superuser:
							return HttpResponseRedirect(reverse('admin_users'))
							
					else:
						messages.error(request,'Invalid credentials.')
						return HttpResponseRedirect(reverse('web_login'))
			else:
				messages.error(request,'Incorrect email and password.')
				return HttpResponseRedirect(reverse('web_login'))

		except Exception as e:
			print(str(e))
			messages.info(request,'No such account exist.')
			return HttpResponseRedirect(reverse('web_login'))


class UserInfo(View):
	template_name = 'artist_info.html'

	def get(self,request):
		user_info = UserDetail.objects.filter(user = request.user).last()
		return render(request,self.template_name,locals())


""" 
	listener user list 
							"""
class ListenerUsers(View):
	template_name = 'listener_users.html'

	def get(self,request):
		users = UserDetail.objects.filter(is_listener = True)
		return render(request,self.template_name,locals())


""" 
	Artist user list 
					  """
class ArtistUsers(View):
	template_name = 'artist_users.html'

	def get(self,request):
		users = UserDetail.objects.filter(is_artist = True)
		return render(request,self.template_name,locals())


""" 
	Admin user list 
					  """
class AdminUsers(View):
	template_name = 'admin-users.html'

	def get(self,request):
		users = User.objects.filter(is_staff = True)
		return render(request,self.template_name,locals())


""" 
	 GenreList list 
					"""
class GeneresList(View):
	template_name = 'genre_list.html'

	def get(self,request):
		genre_list = Genre.objects.all()
		return render(request,self.template_name,locals())



""" Add New Songs """
class AddNewSongs(View):
	template_name = 'add-new-songs.html'

	def get(self,request):
		return render(request,self.template_name,locals())



""" Admin profile """
class AdminProfile(View):
	template_name = 'admin-profile.html'

	def get(self,request):
		return render(request,self.template_name,locals())
	

""" Add New Admin """
class AddAdmin(View):
	template_name = 'add-new-admin.html'

	def get(self,request):

		return render(request,self.template_name,locals())	

	def post(self,request):
		username = request.POST.get('user_name')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		status = request.POST.get('status')
		address = request.POST.get('address')
		phone_number = request.POST.get('phone')

		try:
			user = User.objects.get(Q(username = username)|Q(email = email))
			messages.info(request, "User already exist.")
		except User.DoesNotExist:
			add_user = User.objects.create(
				username = username,
				email = email,
				first_name = first_name,
				last_name = last_name
				)
			add_user.set_password(password)
			if status == "A":
				add_user.status = True
			else:
				add_user.status = False
			add_user.is_staff = True
			add_user.save()

			extra_detail = AdminDetail.objects.create(
				user = add_user,
				phone_number = phone_number,
				address = address
				)

			messages.info(request, "User successfully added.")
		return HttpResponseRedirect(reverse('add_admin'))



""" Add New Album """
class AddAlbum(View):
	template_name = 'add-album.html'

	def get(self,request):
		return render(request,self.template_name,locals())	


""" Add New Playlist """
class Financial(View):
	template_name = 'finacial.html'

	def get(self,request):
		return render(request,self.template_name,locals())	


""" Add New Playlist """
class AddNewPlaylist(View):
	template_name = 'add-playlist.html'

	def get(self,request):
		artist_user = UserDetail.objects.filter(is_artist = True)
		return render(request,self.template_name,locals())

	def post(self,request):
		title = request.POST.get('title')
		artist = request.POST.get('artist')
		cover_img = request.FILES.get('cover_img')
		discription = request.POST.get('discription')

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
			add_play_list.save()
			messages.info(request, "Playlist successfully added.")

		except Exception as e:
			print(e)
			messages.error(request, "Something went wrong.Please try again.")
		return HttpResponseRedirect(reverse('add_new_playlist'))



""" Add New Playlist """
class AllPlayList(View):
	template_name = 'playlist.html'

	def get(self,request):
		playlists = Playlist.objects.all()
		return render(request,self.template_name,locals())


""" Add New Playlist """
class PromostionView(View):
	template_name = 'promostion.html'

	def get(self,request):
		return render(request,self.template_name,locals())

		
""" Add New Playlist """
class ReportUserView(View):
	template_name = 'report-user.html'

	def get(self,request):
		return render(request,self.template_name,locals())

""" Add New Playlist """
class ReportView(View):
	template_name = 'report.html'

	def get(self,request):
		return render(request,self.template_name,locals())


""" Add New Playlist """
class SubscriptionView(View):
	template_name = 'subscrption-offers.html'

	def get(self,request):
		return render(request,self.template_name,locals())


""" Add New Playlist """
class AddGenre(View):
	template_name = 'genre-add.html'

	def get(self,request):
		return render(request,self.template_name,locals())
