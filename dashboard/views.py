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
	template_name = 'admin_users.html'

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

