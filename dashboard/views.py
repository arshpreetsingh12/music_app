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


class HomePage(View):
	template_name = 'dashbaord.html'

	def get(self,request):
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
		return render(request,self.template_name,locals())


""" Add New Playlist """
class AllPlayList(View):
	template_name = 'playlist.html'

	def get(self,request):
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
