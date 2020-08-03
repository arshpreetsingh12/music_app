from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from rest_framework import generics
import uuid, re


""" 
	User can Register their account with this view.
													""" 

class RegisterAPIView(APIView):
	authentication_classes = ()
	def post(self, request):
		context = {}

		data = {
			'first_name': request.data.get('first_name'),
			'username': request.data.get('username'),
			'password': request.data.get('password'),
			'email': request.data.get('email'),

		}
		serializer = UserSerializer(data=data)
		if serializer.is_valid():

			user = serializer.save()
			if user:
				gender = request.data.get('gender')
				date_of_birth = request.data.get('date_of_birth')
				is_artist = request.data.get('is_artist')
				is_listener = request.data.get('is_listener')
				# artist_id = request.data.get('artist_id')
				profile_pic = request.data.get('profile_pic')
				country = request.data.get('country_id')
				website = request.data.get('website')
				company_label = request.data.get('company_label')
				social_media = request.data.get('social_media')
				genre_id = request.data.get('genre_id')

				if not gender:
					user.delete()
					context['success'] = False
					context['message'] = 'Please enter gender'
					return Response(context)
				if not date_of_birth:
					user.delete()
					context['success'] = False
					context['message'] = 'Please enter date of birth'
					return Response(context)

				if not is_artist and not is_listener:
					user.delete()
					context['success'] = False
					context['message'] = 'Please specify user role'
					return Response(context)

				uploader = False
				if is_artist == '1' or is_artist == True:
					uploader = True

					if country is None:
						user.delete()
						context['success'] = False
						context['message'] = 'Please enter your country.'
						return Response(context) 

					if not website:
						user.delete()
						context['success'] = False
						context['message'] = 'Please enter your website.'
						return Response(context) 

					if not company_label:
						user.delete()
						context['success'] = False
						context['message'] = 'Please enter your company label'
						return Response(context) 

					if not social_media:
						user.delete()
						context['success'] = False
						context['message'] = 'Please enter your social media link.'
						return Response(context) 

					if not genre_id:
						user.delete()
						context['success'] = False
						context['message'] = 'Please enter genre_id.'
						return Response(context) 

				else:
					uploader = False

				artists = ""
				normal = False
				if is_listener == '1' or is_listener == True:
					normal = True

					# if artist_id:
					# 	artists = artist_id.split(',')
					# 	if len(artists) < 3:
					# 		user.delete()
					# 		context['success'] = False
					# 		context['message'] = 'Please choose minimum 3 artist.'
					# 		return Response(context)
					
					# else:
					# 	user.delete()
					# 	context['success'] = False
					# 	context['message'] = 'Please choose artist.'
					# 	return Response(context)

				else:
					normal = False

				user_detail = UserDetail(
					user_id = user.id,
					gender = gender,
					date_of_birth=date_of_birth,
					is_artist = uploader,
					is_listener = normal
					)
				if profile_pic:
					user_detail.profile_pic = profile_pic
				user_detail.save()
				print(user_detail)

				genre_obj = ''
				if genre_id:
					try:
						genre_obj = Genre.objects.get(pk = genre_id)
					except Genre.DoesNotExist:
						user.delete()
						user_detail.delete()
						context['success'] = False
						context['message'] = 'Invalid genre id.'
						return Response(context) 

				country_obj = ""
				if country:
					try:
						country_obj = Country.objects.get(pk = country)
					except Country.DoesNotExist:
						user.delete()
						user_detail.delete()
						context['success'] = False
						context['message'] = 'Invalid country id.'
						return Response(context) 

				if country_obj and website and company_label and genre_id and social_media and user_detail.is_artist == True:
					artist_info = ArtistInfo(
						info = user_detail,
						website = website,
						company_label = company_label,
						social_media = social_media,
						genre = genre_obj,
						country = country_obj
						)
					artist_info.save()

				# if artists and user_detail.is_listener:
				# 	for art in artists:
				# 		LikeArtist.objects.create(
				# 			user = user,
				# 			artist_id = art,
				# 			like = True		
				# 			)
				context['success'] = True
				context['message'] = 'You signed up successfully.'

		else:
			context['success'] = False
			context['error'] = 	serializer.errors				

		return Response(context)	


""" Country List """ 
class CountryList(APIView):
	def get(self, request):
		context = {}
		try:
			qs = Country.objects.all()
			if qs:
				serializer = CountrySerializser(qs, many=True)
				context['success'] = True
				context['data'] = serializer.data
			else:
				context['success'] = True
				context['message'] = "No country found."
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)	


""" Country List """ 
class GenreList(APIView):
	def get(self, request):
		context = {}
		genre_name = request.GET.get('genre_name')
		try:
			if not genre_name:
				qs = Genre.objects.all()
				if qs:
					serializer = GenreSerializer(qs, many=True)
					context['success'] = True
					context['data'] = serializer.data
				else:
					context['success'] = True
					context['message'] = "No Genre found.aaa"
			else:
				searched_genre = re.sub("\s+$","",genre_name)
				qs = Genre.objects.filter(genre__icontains = searched_genre)
				if qs:
					serializer = GenreSerializer(qs, many=True)
					context['success'] = True
					context['data'] = serializer.data
				else:
					context['success'] = True
					context['message'] = "No Genre foundssss."
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)	

""" Login View """ 
class LoginAPIView(ObtainAuthToken):
	authentication_classes = ()
	def post(self, request):
		context = {}
		try:
			print(request.data)
			username = request.data.get('username')
			password = request.data.get('password')
			if not username or not password:
				context['status'] = False
				context['message'] = 'username and password both fields are required'
				return Response(context)
			user = authenticate(username=username, password=password)

			if user:
				token, created = Token.objects.get_or_create(user=user)
				context['status'] = True
			
				if user.is_superuser or user.is_staff:
					context['is_superuser'] = True

				user_obj = UserDetail.objects.get(user = user)

				if user_obj.is_listener and not user_obj.is_artist:
					artist_users = UserDetail.objects.filter(is_artist = True)
					# serializer = UserDetailSerializer(artist_users, many=True)
					# context['artist'] = serializer.data
				
				if user_obj.is_artist or user_obj.is_listener:
					user_data = {
						'username': user.username,
						'full_name': user.first_name,
						'email': user.email,
						'is_artist':user_obj.is_artist,
						'is_listener':user_obj.is_listener,
						'profile_pic':user_obj.profile_pic.url

					}
					context['user'] = user_data

				if user_obj.is_listener:
					liked_artist = LikeArtist.objects.filter(user = user, like = True)
					if liked_artist:
						liked = LikeArtistSerializer(liked_artist, many=True)
						context['selected_artist_data'] = liked.data 
					playlists = Playlist.objects.filter(user = user).count()
					followers = Follwer.objects.filter(following_user = user).count()
					following = Follwer.objects.filter(follower_user = user).count()
					other_data = {
						'playlists':playlists,
						'followers':followers,
						'following':following,
					}
					context['other_data'] = other_data

				if user_obj.is_artist:
					social_media = {
						'website':user_obj.artistinfo.website,
						'company_label':user_obj.artistinfo.company_label,
						'social_media':user_obj.artistinfo.social_media,
					}
					context['social_media'] = social_media	
				context['message'] = 'Successfully login.'
				context['data'] = {'token': token.key}
				login(request, user)
		
			else:
				context['status'] = False
				context['message'] = 'Invalid credentials.'
		
		except Exception as e:
			context['status'] = False
			context['message'] = 'Something went wrong, Please try again.'
		return Response(context)

""" 
	Logged out view.
    				 """ 

class LogoutAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		try:
			print(request.user)
			request.user.auth_token.delete()
			context['token'] = 'Token deleted'
		except Exception as e:
			context['success'] = False
			context['message'] = 'Cannot access token'
		logout(request)
		context['success'] = True	
		context['message'] = 'You have been logged out'
		return Response(context)
			
""" 
	Logged in user can edit their profile.
    						  			   """ 
class EditUserAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permissions_classes = [IsAuthenticated]
	def put(self, request):
		context = {}

		if not request.data:
			context['success'] = False	
			context['message'] = 'Please enter detail you want to change.' 
			return Response(context)

		date_of_birth = request.data.get('date_of_birth')
		gender = request.data.get('gender')
		profile_pic = request.data.get('profile_pic')
		website =  request.data.get('website')
		company_label = request.data.get('company_label')
		social_media = request.data.get('social_media')
		country = request.data.get('country')
		genre = request.data.get('genre')

		try:
			user = UserDetail.objects.get(user_id=request.user.id)
			if date_of_birth:
				user.date_of_birth = date_of_birth
			if gender:
				user.gender = gender
			if profile_pic:
				user.profile_pic = profile_pic
			user.save()

			if user.is_artist:
				updateart = ArtistInfo.objects.get(info = user) 
				if website:
					updateart.website = website
				if company_label:
					updateart.company_label = company_label
				if social_media:
					updateart.social_media = social_media
				if country:
					try:
						country_obj = Country.objects.get(pk = country)
						updateart.country = country_obj
					except Country.DoesNotExist:
						context['success'] = False
						context['message'] = 'Invalid country id.'
						return Response(context)

				if genre:
					try:
						genre_obj = Genre.objects.get(pk = genre)
						updateart.genre = genre_obj
					except Genre.DoesNotExist:
						context['success'] = False
						context['message'] = 'Invalid genre id.'
						return Response(context) 
				updateart.save() 

			serializer = UserSerializer(request.user, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				context['success'] = True	
				context['message'] = 'Profile successfully updated.' 
			else:
				context['success'] = False	
				context['error'] = serializer.errors 
		except Exception as e:
			context['success'] = False	
			context['message'] = str(e)
		return Response(context)


""" 
	Logged in user can edit their profile.
    						  			   """ 
class UserInformation(APIView):
	authentication_classes = (TokenAuthentication,)
	permissions_classes = [IsAuthenticated]
	def get(self, request):
		context = {}
		
		try:
			user = UserDetail.objects.get(user_id=request.user.id)
			# serializer = UserSerializer(request.user)
			userdetail = UserDetailSerializer(user)
			context['status'] = True
			data = {
				'first_name':user.user.first_name,
				'username':user.user.username,
				 "email": user.user.email,
			}	
			context['data'] = data
			context['detail'] =  userdetail.data
			if user.is_artist:
				artist_info = ArtistInfo.objects.get(info = user)
				artist = ArtistInfoSerializer(artist_info)
				context['artist_info'] = artist.data

			liked_artist = LikeArtist.objects.filter(user = request.user, like = True)
			if liked_artist:
				liked = LikeArtistSerializer(liked_artist, many=True)
				context['selected_artist_data'] = liked.data 

		except Exception as e:
			context['status'] = False	
			context['message'] = "Something went wrong."
		return Response(context)				

""" 
	This view for add song. 
    Only uploader can add songs. 
    							""" 
class SongsAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self, request):
		context = {}
		try:
			if not request.user.is_superuser or not request.user.is_staff:
				user = UserDetail.objects.get(user_id = request.user.id)
				if user.is_artist:
					qs = Song.objects.filter(user = user, delete = False)
				else:
					qs = Song.objects.filter(delete = False)
			else:
				qs = Song.objects.filter(delete = False)
			if not qs:
				context['success'] = True
				context['data'] = "Songs not found."		
				return Response(context)
			serializer = SongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)	

	def post(self, request):
		context = {}
		genre_id = request.data.get('genre_id')
		song_title = request.data.get('song_title')
		song_mp3 = request.data.get('song_mp3')
		song_image = request.data.get('song_image')
		song_length = request.data.get('song_length')
		description = request.data.get('description')

		if not genre_id or not song_title or not song_mp3 or not song_length:
			context['success'] = False
			context['message'] = 'song_title, genre_id, song_mp3, song_length and artist_id are required fields.'
			return Response(context)

		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist:
				data = {
					'user': user.id,
					'genre': genre_id,
					'song_title':song_title,
					'song_mp3': song_mp3,
					'song_image':song_image,
					'song_length':song_length,
					'description':description
				}
				serializer = SongSerializer(data=data)
				if serializer.is_valid():
					serializer.save()
					context['success'] = True
					context['message'] = 'Song successfully added.'
				else:
					context['success'] = False
					context['error'] = serializer.errors
			else:
				context['success'] = False
				context['error'] = "You don't have permission to add song."
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong. Please try again.'
		return Response(context)	

	def delete(self, request):
		dictV = {}
		data = request.data.get('id')
		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist:
				if data:
				    obj = Song.objects.get(pk=data,user = user, delete=False)
				    obj.delete = True
				    obj.save()
				    status = True
				    message = 'Song successfully deleted.'
				else:
					status = False
					message = 'Id is required.'
			else:
				status = False
				message = "You don't have permission to delete song."
		except Song.DoesNotExist:
		    status = True
		    message = 'Song does not exist.'

		
		dictV['status'] = status
		dictV['message'] = message
		return Response(dictV)


	def put(self, request):
		dictV = {}
		song_id = request.data.get('id')
		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist:
				if song_id:
				    obj = Song.objects.get(pk=song_id,user_id = request.user.id, delete=False)
				    serializer = SongSerializer(obj, data=request.data, partial=True)
				    if serializer.is_valid():
				    	serializer.save()
				    	status = True
				    	message = 'Song successfully updated.'
				    else:
				    	status = False
				    	message = serializer.errors
				else:
					status = False
					message = 'Id is required.'
			else:
				status = False
				message = "You don't have permission to add song."
		except Song.DoesNotExist:
		    status = True
		    message = 'Song does not exist.'
	
		dictV['status'] = status
		dictV['message'] = message
		return Response(dictV)
	

"""
	This view for artist list.
							 """
class AllArtist(APIView):

	def get(self, request):
		context = {}
		artist_name = request.GET.get('artist_name')
		try:
			if not artist_name:
				qs = ArtistInfo.objects.all()
				if not qs:
					context['success'] = True
					context['message'] = "Artist not found."		
					return Response(context)
				serializer = AllArtistDataSerializer(qs, many=True)
				context['success'] = True
				context['data'] = serializer.data	

			else:
				searched_artist = re.sub("\s+$","",artist_name.lstrip())
				artist_info = ArtistInfo.objects.filter(info__user__first_name__icontains = searched_artist, info__is_artist = True)
				if artist_info:
					serializer = AllArtistDataSerializer(artist_info, many = True)
					context['status'] = True
					context['data'] = serializer.data
				else:
					context['status'] = True
					context['message'] = "No artist found."

		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong '

		return Response(context)



"""
	This view for found artist by artist.
							 				"""
class ArtistDetail(APIView):

	def get(self, request, pk):
		context = {}
		try:
			qs = ArtistInfo.objects.get(pk = pk)
			# qs = UserDetail.objects.get(pk = pk, is_artist = True)
			# serializer = UserDetailSerializer(qs)
			serializer = AllArtistDataSerializer(qs)
			context['status'] = True
			context['data'] = serializer.data

		except UserDetail.DoesNotExist:
			context['status'] = False
			context['message'] = 'Invalid artist id.'	

		except Exception as e:
			context['status'] = False
			context['message'] = 'Something went wrong '+str(e)
		return Response(context)


"""
	This view for like artist.
	Logged in user can like any artist.
									    """
class LikeArtistAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			qs = LikeArtist.objects.filter(user_id=user_id, like = True)
			if not qs:
				context['success'] = True
				context['data'] = "Liked artist not found."		
				return Response(context)
			serializer = LikeArtistSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)	

	def put(self, request):
		context = {}
		artist_id= request.data.get('artist_id')
	
		if artist_id:
			artists = artist_id.split(',')
			check_liked_artist = LikeArtist.objects.filter(user_id = request.user.id, like = True).count()
			if check_liked_artist == 0:

				if len(artists) >= 3:
					for art in artists:
						try:
							check_ar = ArtistInfo.objects.get(pk = art)
							liked_artist,created = LikeArtist.objects.get_or_create(user_id = request.user.id,artist = check_ar, like = True)
							context['success'] = True
							context['message'] = 'Artist successfully liked.'
							# liked_artist = LikeArtist.objects.filter(user_id = request.user.id,artist_id = art, like = True).last()
							
							# data = {
							# 	'user': request.user.id,
							# 	'artist': art,
							# 	'like': True
							# }

							# try:
							# 	serializer = LikeArtistSerializer(data=data)
							# 	if serializer.is_valid():
							# 		serializer.save()
							# 		context['success'] = True
							# 		context['message'] = 'Artist successfully liked.'
							# 	else:
							# 		context['success'] = False
							# 		context['error'] = serializer.errors
							# except Exception as e:
							# 	context['success'] = False
							# 	context['message'] = 'Something went wrong, Please try again.'
							# # else:
							# # 	context['success'] = False
							# # 	context['message'] = 'Artist already liked.'

						except ArtistInfo.DoesNotExist:
							context['success'] = False
							context['message'] = 'Invalid artist id.'

				else:
					context['status'] = False
					context['message'] = 'Please choose minimum 3 artist.'

			else:
				for art in artists:
					try:
						check_ar = ArtistInfo.objects.get(pk = art)
						liked_artist,created = LikeArtist.objects.get_or_create(user_id = request.user.id,artist = check_ar, like = True)
						context['success'] = True
						context['message'] = 'Artist successfully liked.'
						
						# data = {
						# 	'user': request.user.id,
						# 	'artist': art,
						# 	'like': True
						# }

						# try:
						# 	serializer = LikeArtistSerializer(data=data)
						# 	if serializer.is_valid():
						# 		serializer.save()
						# 		context['success'] = True
						# 		context['message'] = 'Artist successfully liked.'
						# 	else:
						# 		context['success'] = False
						# 		context['error'] = serializer.errors
						# except Exception as e:
						# 	context['success'] = False
						# 	context['message'] = 'Something went wrong, Please try again.'

						# else:
						# 	context['success'] = False
						# 	context['message'] = 'Artist already liked.'
					except ArtistInfo.DoesNotExist:
						context['success'] = False
						context['message'] = 'Invalid artist id.'						
		
		else:
			context['success'] = False
			context['message'] = 'Artist id is required filed.'
		return Response(context)


class DislikeArtist(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def post(self, request):
		context = {}
		artist_id = request.data.get('artist_id')
		user_id = request.user.id
		
		try:
			if artist_id:
				artists = artist_id.split(',')
				for art in artists:
					qs = LikeArtist.objects.get(artist_id = art, user_id = user_id, like = True)
					qs.like = False
					qs.save()
					context['success'] = True
					context['data'] = "Successfully dislike artist."	
			else:
				context['success'] = False
				context['data'] = "Please select any artist."
		except Exception as e:
			context['success'] = False
			context['message'] = 'Artist not found.'	
		return Response(context)

"""
	This view for liked artist's songs.
										"""
class SongsOfLikedArtistAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			liked_artist_qs = LikeArtist.objects.filter(user_id=user_id)
			liked_artist_ids = [artist.artist_id for artist in liked_artist_qs]
			qs = Song.objects.filter(album__artist_id__in=liked_artist_ids,delete = False)
			if not qs:
				context['success'] = True
				context['data'] = "Songs not found."		
				return Response(context)
			serializer = SongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
	
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)					
	
"""
	This view for Like song.
	Logged in user can like any song.
									   """
class LikeSongAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permissions_classes = [IsAuthenticated]

	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			qs = LikeSong.objects.filter(user_id=user_id, like = True)
			if not qs:
				context['success'] = False
				context['data'] = "Songs not found."		
				return Response(context)
			serializer = LikeSongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)


	def post(self, request):
		context = {}
		user = request.user.id
		song_id = request.data.get('song_id')

		try:
			if song_id:
				data = {
					'user':user,
					'song': song_id,
					'like': True 
				}
				serializer = LikeSongSerializer(data=data)
				if serializer.is_valid():
					serializer.save()
					context['success'] = True
					context['message'] = 'Song successfully liked.'
				else:
					context['success'] = False
					context['error'] = serializer.errors

			else:
				context['success'] = False
				context['error'] = "Song id is required."

		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)

"""
	This view for add album.Only uploader can add album.
							                             """
class AddAlbumAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			if not request.user.is_superuser or not request.user.is_staff:
				user = UserDetail.objects.get(user_id = user_id)
				if user.is_artist:
					qs = Album.objects.filter(artist = user, is_deleted = False)
				else:
					qs = Album.objects.filter(is_deleted = False)
			else:
				qs = Album.objects.filter(is_deleted = False)
			if not qs:
				context['success'] = False
				context['data'] = "album not found."		
				return Response(context)
			serializer = AlbumSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data	
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)

	def post(self, request):
		context = {}
		artist_id = request.data.get('artist_id')
		album_name = request.data.get('album_name')
		album_pic = request.data.get('album_pic')
		fb_url = request.data.get('fb_url')
		twitter_url = request.data.get('twitter_url')
		google_url = request.data.get('google_url')
		website_url = request.data.get('website_url')
		description = request.data.get('description')
		song_id = request.data.get('song_id')
		album_length = request.data.get('album_length')

		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist: 
				if album_name and song_id:

					songs = song_id.split(',')

					data = {
						'artist': user.id,
						'album': album_name,
						'album_pic': album_pic,
						'fb_url':fb_url,
						'twitter_url':twitter_url,
						'google_url':google_url,
						'website_url':website_url,
						'description':description,
						'song':songs,
						'album_length':album_length
					}
					serializer = AlbumSerializer(data=data)
					if serializer.is_valid():
						serializer.save()
						context['success'] = True
						context['message'] = 'Album successfully added.'
					else:
						context['success'] = False
						context['error'] = serializer.errors
				else:
					context['success'] = False
					context['error'] = "song id and album fields are required."
			else:
				context['success'] = False
				context['error'] = "You don't have permission to add album."
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong.'		
		return Response(context)


	def delete(self, request):
		dictV = {}
		album_id = request.data.get('album_id')
		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist: 
				if album_id:
					album_obj = Album.objects.get(pk = album_id,artist = user)
					album_obj.is_deleted = True
					album_obj.save()
					dictV['status'] = True
					dictV['data'] = "Album successfully deleted."
				else:
					dictV['status'] = False
					dictV['error'] = "Id is required."
			else:
				context['success'] = False
				context['error'] = "You don't have permission to add album."
		except Album.DoesNotExist:
			dictV['status'] = False
			dictV['data'] = "Album does not exist."

		except Exception as e:
			dictV['status'] = False
			dictV['error'] = "Something went wrong, Please try again."
		return Response(dictV)


	def put(self, request):
		dictV = {}
		album_id = request.data.get('album_id')
		song_id = request.data.get('song_id')
		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist:
				if album_id:
				    obj = Album.objects.get(pk = album_id, artist = user)
				    serializer = AlbumSerializer(obj, data=request.data, partial=True)
				    if serializer.is_valid():
				    	serializer.save()
				    	status = True
				    	message = 'Album successfully updated.'

				    else:
				    	status = False
				    	message = serializer.errors
				else:
					status = False
					message = 'Id is required.'
			else:
				status = False
				message = "You don't have permission to update album."
		except Album.DoesNotExist:
		    status = True
		    message = 'Album does not exist.'
	
		dictV['status'] = status
		dictV['message'] = message
		return Response(dictV)

class AlbumDetail(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self, request, album_id):
		context = {}
		user_id = request.user.id
		qs = ''
		try:
			if not request.user.is_superuser or not request.user.is_staff:
				user = UserDetail.objects.get(user_id = user_id)
				if user.is_artist:
					qs = Album.objects.get(pk = album_id,artist = user,is_deleted = False)
				else:
					qs = Album.objects.get(pk = album_id,is_deleted = False)
			else:
				qs = Album.objects.get(pk = album_id,is_deleted = False)
			
			if not qs:
				context['status'] = True
				context['data'] = "No album found."		
				return Response(context)
			album = AlbumSerializer(qs)
			context['status'] = True
			context['album'] = album.data

		except Exception as e:
			context['status'] = False
			context['message'] = "Invalid album id."
		return Response(context)

"""
	This view for get songs.
	User can get songs according to artist, album or genre.
							                         		 """
class GetSongsAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def post(self, request):		
		context = {}
		artist_id = request.data.get('artist_id')
		album_id = request.data.get('album_id')
		genre_id = request.data.get('genre_id')
		try:
			if artist_id and album_id:
				qs = Song.objects.filter(album_id=album_id, album__artist_id=artist_id, delete = False)	
			elif artist_id:
				qs = Song.objects.filter(album__artist_id=artist_id, delete = False)
			elif album_id:	
				qs = Song.objects.filter(album_id=album_id, delete = False)
			elif genre_id:
				qs = Song.objects.filter(genre_id=genre_id, delete = False)
			else:
				qs = Song.objects.filter(delete = False).order_by('-id') # recent one	
			serializer = SongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)


"""
	Send login link.
				    """
class SendLoginLinkAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		email = request.data.get('email')
		if not email:
			context['success'] = False
			context['message'] = "Please enter email"
			return Response(context)	
		try:
			user = User.objects.get(email=email)
			subject = 'Login Link'
			link = settings.BASE_URL+"/api/login"
			recipient = [email]
			message = f""" \r\n

			Please click on this link to login \r\n

					{link} \r\n

			"""
			status = mailSend(subject, recipient, message)
			if status:
				context['success'] = True
				context['message'] = 'Please check your mail for more information.'
			else:
				context['success'] = False
				context['message'] = "Some error occur. Retry or contact with administrator."
		except User.DoesNotExist:
			context['success'] = False
			context['message'] = "This email address is not registred."	
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)



def mailSend(subject, recipient_list, message="", html_message=""):
	try:
		email_from = settings.EMAIL_HOST_USER
		print(html_message)
		send_mail( subject, message, email_from, recipient_list, html_message=html_message )
		return True
	except Exception as e:
		return False	



"""
	This view for change password.
							 		"""
class ChangePasswordApi(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def put(self, request):		
		context = {}
		new_password = request.data.get('new_password')
		try:
			if new_password:
				user = User.objects.get(pk = request.user.id)
				user.set_password(new_password)
				user.save()
				context['status'] = True
				context['message'] = 'Password successfully updated.'

			else:
				context['status'] = False
				context['message'] = 'Please enter new password'	
		except Exception as e:
			context['status'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)


"""
	Send forget password link.
				    			"""
class ForgetPasswordLinkAPIView(APIView):
	permission_classes = [AllowAny]
	def get(self, request):
		context = {}
		email = request.GET.get('email')
		if not email:
			context['status'] = False
			context['message'] = "Please enter email"
			return Response(context)	
		try:
			activation_key = str(uuid.uuid4())[:18].replace("-", "")
			user = User.objects.get(email=email)
			data = {
				'user':user.id,
				'activation_key':activation_key
			}
			fg_pwd = ForgetPasswordSerializser(data = data)

			if fg_pwd.is_valid():
				fg_pwd.save()

				subject = 'Reset Password Link'
				link = settings.BASE_URL+"/api/reset-password"
				recipient = [email]
				message = f""" \r\n

				Please click on this link to reset password \r\n
				activation link {activation_key} \r\n

						{link} \r\n

				"""

				mail_status = mailSend(subject, recipient, message)
				if mail_status:
					context['status'] = True
					context['message'] = 'Please check your mail for more information.'
				else:
					context['status'] = False
					context['message'] = "Some error occur. Retry or contact with administrator."
			else:
				context['status'] = False
				context['error'] = fg_pwd.errors
			
		
		except User.DoesNotExist:
			context['status'] = False
			context['message'] = "This email address is not registred."	
		except Exception as e:
			context['status'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)


"""
	Reset password
				    """
class ResetPasswordAPIView(APIView):

	def post(self, request):
		context = {}
		activation_key = request.data.get('activation_key')
		new_password = request.data.get('new_password')

		if not activation_key:
			context['status'] = False
			context['message'] = "Please enter activation_key"
			return Response(context)

		if not new_password:
			context['status'] = False
			context['message'] = "Please enter password"
			return Response(context)
		try:
			fg_pwd = ForgetPassword.objects.get(activation_key = activation_key)
			user = User.objects.get(email = fg_pwd.user.email)
			user.set_password(new_password)
			user.save()
			fg_pwd.delete()
			context['status'] = True
			context['message'] = 'Password successfully changed.'						
		
		except ForgetPassword.DoesNotExist:
			context['status'] = False
			context['message'] = "Invalid activation key."	
		except Exception as e:
			context['status'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)


"""
	This view for hide songs.
							  """
class HideSongAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self, request):
		context = {}
		try:
			qs = HideSong.objects.filter(user_id=request.user.id)
			serializer = HideSongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)	

	def post(self, request):
		context = {}
		song_id = request.data.get('song_id')
		data = {
			'user':request.user.id,
			'song': song_id,
			'hide': True
		}

		try:
			serializer = HideSongSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				context['success'] = True
				context['message'] = 'Song is hidden now.'
			else:
				context['success'] = False
				context['error'] = serializer.errors	
		except User.DoesNotExist:
			context['success'] = False
			context['message'] = "User doesn't exist"	
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)


"""
	This view for create Playlist.
	Logged in user can create their playlist.
							      			   """
class CreatePlaylistAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self, request):
		context = {}
		try:
			qs = Playlist.objects.filter(user_id=request.user.id)
			if qs:
				serializer = PlaylistSerializer(qs, many=True)
				context['success'] = True
				context['data'] = serializer.data
			else:
				context['success'] = True
				context['message'] = "User have no Playlist."
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)	

	def post(self, request):
		context = {}
		playlist = request.data.get('playlist')
		if playlist:
			data = {
				'user': request.user.id,
				'playlist': playlist,
			}

			try:
				serializer = PlaylistSerializer(data=data)
				if serializer.is_valid():
					serializer.save()
					context['success'] = True
					context['message'] = 'Playlist successfully created.'
				else:
					context['success'] = False
					context['error'] = serializer.errors	
	
			except Exception as e:
				context['success'] = False
				context['message'] = "Something went wrong, Please try again"
		else:
			context['success'] = False
			context['message'] = "Playlist name is required."	
		return Response(context)	


"""
	This view for add songs in Playlist.
							      	     """

class PlaylistTrackAPIView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def post(self, request):
		context = {}
		playlist_id = request.data.get('playlist_id')
		song_id = request.data.get('song_id')
		
		if not playlist_id or not song_id:
			context['success'] = False
			context['message'] = "playlist_id and song_id both are required fields."
			return Response(context)
		data = {
			'user': request.user.id,
			'playlist': playlist_id,
			'song': song_id
		}		 

		try:
			serializer = PlaylistTrackSerializser(data=data)
			if serializer.is_valid():
				serializer.save()
				context['success'] = True
				context['message'] = 'Song successfully added in playlist.'
			else:
				context['success'] = False
				context['error'] = serializer.errors	
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)

"""
	This view for get list of songs from playlist.
							      	     		   """

class ListSongsByPlaylistAPIView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def post(self, request):
		context = {}
		playlist_id = request.data.get('playlist_id')
		if not playlist_id:
			context['success'] = False
			context['message'] = "Playlist id is required."	
			return Response(context)

		try:
			qs = PlaylistTrack.objects.filter(playlist_id=playlist_id)
			if not qs:
				context['success'] = True
				context['message'] = "Playlist not found."	
				return Response(context)

			serializer = PlaylistTrackSerializser(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)	

########## for logged in artist user ############


"""
	All User's list.
					   """

class UserList(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def get(self,request):
		dictV = {}
		try:
			users = User.objects.all().exclude(pk = request.user.id)
			if users:
				serializer = UserSerializer(users, many=True)
				dictV['success'] = True
				dictV['data'] = serializer.data
			else:
				dictV['success'] = True
				dictV['data'] = 'No user found.'
		except Exception as e:
			dictV['success'] = False
			dictV['data'] = "Some thing went wrong."
		return Response(dictV)


################### For normal user  ##########################

"""
	Logged in user's follower list.
					   				"""
class MyFollowerList(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get(self,request):
		dictV = {}
		try:
			follwers = Follwer.objects.filter(following_user_id = request.user.id, is_follwed = True)
			if follwers:
				serializer = FollowUserSerializser(follwers, many=True)
				dictV['success'] = True
				dictV['data'] = serializer.data
			else:
				dictV['success'] = True
				dictV['data'] = 'No follower found.'
		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again"	
		return Response(dictV)


"""
 	Logged in user's following list
 									 """
class MyFollowingList(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def get(self,request):
		dictV = {}
		try:
			following = Follwer.objects.filter(follower_user_id = request.user.id, is_follwed = True)
			if following:
				serializer = FollowUserSerializser(following, many=True)
				dictV['success'] = True
				dictV['data'] = serializer.data
			else:
				dictV['success'] = True
				dictV['data'] = 'No following found.'
		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again"	
		return Response(dictV)

	def post(self,request):
		dictV = {}
		following_user_id = request.data.get('id')
		if not following_user_id:
			dictV['success'] = False
			dictV['message'] = "Id field is required."
			return Response(dictV)	
	
		if following_user_id == request.user.id:
			dictV['success'] = False
			dictV['message'] = "Please enter another user id."
			return Response(dictV)

		try:
			follwers = Follwer.objects.get(follower_user_id = request.user.id, following_user = following_user_id, is_follwed = True)
			dictV['success'] = False
			dictV['message'] = "You already follow this user."
			return Response(dictV)
		except Follwer.DoesNotExist:
			pass

		data = {
			'follower_user': request.user.id,
			'following_user': following_user_id,
			'is_follwed': True
		}
		try:
			serializer = FollowUserSerializser(data=data)
			if serializer.is_valid():
				serializer.save()
				dictV['success'] = True
				dictV['message'] = 'Now you started following this user.'
			else:
				dictV['success'] = False
				dictV['error'] = serializer.errors	
		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again"	
		return Response(dictV)


class ValidateToken(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]
	def get(self, request):
		context = {}
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			token = token.split()
			if len(token) == 1 or len(token) > 2:
				context['status'] = False
				context['message'] = 'Invalid secrer key header. No credentials provided.'
		
			else:
				token = Token.objects.get(key=token[1])
				context['status'] = True
			
				if token.user.is_superuser or token.user.is_staff:
					context['is_superuser'] = True

				user_obj = UserDetail.objects.get(user = token.user)

				if user_obj.is_listener and not user_obj.is_artist:
					artist_users = UserDetail.objects.filter(is_artist = True)
				
				if user_obj.is_artist or user_obj.is_listener:
					user_data = {
						'username': token.user.username,
						'full_name': token.user.first_name,
						'email': token.user.email,
						'is_artist':user_obj.is_artist,
						'is_listener':user_obj.is_listener,
						'profile_pic':user_obj.profile_pic.url

					}
					context['user'] = user_data	
				if user_obj.is_artist:
					social_media = {
						'website':user_obj.artistinfo.website,
						'company_label':user_obj.artistinfo.company_label,
						'social_media':user_obj.artistinfo.social_media,
					}
					context['social_media'] = social_media

				liked_artist = LikeArtist.objects.filter(user_id = user_obj.user.id, like = True)
				if liked_artist:
					liked = LikeArtistSerializer(liked_artist, many=True)
					context['selected_artist_data'] = liked.data 
					
		except Token.DoesNotExist:
			context['status'] = False
			context['error'] = 'Invalid token provided.'

		except Exception as e:
			context['status'] = False
			context['error'] = 'Something went wrong, Please try again.'
		return Response(context)


