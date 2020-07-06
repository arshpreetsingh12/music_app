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

from .serializers import *
from rest_framework import generics


class HomeAPIView(APIView):
	def get(self, request):
		context = {}
		context['success'] = True
		context['message'] = 'On homepage'
		return Response(context)


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
				is_normal = request.data.get('is_normal')
				
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

				if not is_artist and not is_normal:
					user.delete()
					context['success'] = False
					context['message'] = 'Please specify user role'
					return Response(context)


				uploader = False
				if is_artist:
					uploader = is_artist
				else:
					uploader = False

				normal = True
				if is_normal:
					normal = is_normal
				else:
					normal = False

				user_detail = UserDetail(
					user_id=user.id,
					gender=gender,
					date_of_birth=date_of_birth,
					is_artist = uploader,
					is_normal = normal
					)
				user_detail.save()
				print(user_detail)
				context['success'] = True
				context['message'] = 'You signed up successfully.'

		else:
			context['success'] = False
			context['error'] = 	serializer.errors				

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
				context['success'] = False
				context['message'] = 'username and password both fields are required'
				return Response(context)
			user = authenticate(username=username, password=password)

			if user:
				token, created = Token.objects.get_or_create(user=user)
				context['success'] = True
			
				if user.is_superuser or user.is_staff:
					context['is_superuser'] = True

				user_obj = UserDetail.objects.get(user = user)

				if user_obj.is_normal and not user_obj.is_artist:
					artist_users = UserDetail.objects.filter(is_artist = True)
					serializer = UserDetailSerializer(artist_users, many=True)
					context['user'] = serializer.data
				
				if user_obj.is_artist:
					user_data = {
						'username': user.username,
						'full_name': user.first_name,
						'email': user.email,
						'is_artist':user_obj.is_artist
					}
					context['user'] = user_data
				context['message'] = 'Successfully login.'
				context['data'] = {'token': token.key}
				login(request, user)
		
			else:
				context['success'] = False
				context['message'] = 'Invalid credentials.'
		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong, Please try again.'
		return Response(context)

""" 
	Logged out view.
    				 """ 

class LogoutAPIView(APIView):
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
	permissions_classes = [IsAuthenticated]
	def put(self, request):
		context = {}

		if not request.data:
			context['success'] = False	
			context['message'] = 'Please enter detail you want to change.' 
			return Response(context)

		date_of_birth = request.data.get('date_of_birth')
		gender = request.data.get('gender')
		
		try:

			user = UserDetail.objects.get(user_id=request.user.id)
			if date_of_birth:
				user.date_of_birth = date_of_birth
				user.save()
			if gender:
				user.gender = gender
				user.save()	

			serializer = UserSerializer(request.user, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				print(serializer)	
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
	This view for add song. 
    Only uploader can add songs. 
    							""" 
class SongsAPIView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		context = {}
		genre_id = request.data.get('genre_id')
		album_id = request.data.get('album_id')
		song = request.data.get('song')

		if not genre_id or not album_id or not song:
			context['success'] = False
			context['message'] = 'album_id, genre_id and song are required fields.'
			return Response(context)

		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist:
				data = {
					'user': request.user.id,
					'genre': genre_id,
					'song': song,
					'album': album_id
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
		data = request.data.get('id')
		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist:
				if data:
				    obj = Song.objects.get(pk=data, delete=False)
				    obj.delete = True
				    obj.save()
				    status = True
				    message = 'Song successfully deleted.'
				else:
					status = False
					message = 'Id is required.'
			else:
				context['success'] = False
				context['error'] = "You don't have permission to add song."
		except Song.DoesNotExist:
		    status = True
		    message = 'Song does not exist.'

		dictV = {}
		dictV['status'] = status
		dictV['message'] = message
		return Response(dictV)


"""
	This view for like artist.
	Logged in user can like any artist.
									    """
class LikeArtistAPIView(APIView):
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

	def post(self, request):
		context = {}
		artist_id= request.data.get('artist_id')
		if artist_id:
			try:
				LikeArtist.objects.get(artist_id = artist_id, user_id = request.user.id, like = True)
				context['success'] = False
				context['message'] = 'You already liked this artist.'
				return Response(context)
			except LikeArtist.DoesNotExist:
				pass
			
			data = {
				'user': request.user.id,
				'artist': artist_id,
				'like': True
			}

			try:
				serializer = LikeArtistSerializer(data=data)
				if serializer.is_valid():
					serializer.save()
					context['success'] = True
					context['message'] = 'Artist successfully liked.'
				else:
					context['success'] = False
					context['error'] = serializer.errors
			except Exception as e:
				context['success'] = False
				context['message'] = 'Something went wrong, Please try again.'
		else:
			context['success'] = False
			context['message'] = 'Artist id is required filed.'
		return Response(context)


"""
	This view for liked artist's songs.
										"""
class SongsOfLikedArtistAPIView(APIView):
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
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		artist_id = request.data.get('artist_id')
		album = request.data.get('album')
		album_pic = request.data.get('album_pic')

		try:
			user = UserDetail.objects.get(user_id = request.user.id)
			if user.is_artist: 
				if artist_id and album:
					data = {
						'artist': artist_id,
						'album': album,
						'album_pic': album_pic
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
					context['error'] = "Artist id and album fields are required."
			else:
				context['success'] = False
				context['error'] = "You don't have permission to add album."
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong.'		
		return Response(context)


"""
	This view for get songs.
	User can get songs according to artist, album or genre.
							                         		 """
class GetSongsAPIView(APIView):
	authentication_classes = ()
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
	authentication_classes = ()
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
	This view for hide songs.
							  """
class HideSongAPIView(APIView):
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
	This view for get logged in artist's song list.
							      	     		    """

class ArtistSongList(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		dictV = {}
		try:
			songs = Song.objects.filter(album__artist_id = request.user.id, delete = False)
			if songs:
				serializer = SongSerializer(songs, many=True)
				dictV['success'] = True
				dictV['data'] = serializer.data
			else:
				dictV['success'] = True
				dictV['data'] = 'Songs not found.'
		except Exception as e:
			dictV['success'] = False
			dictV['data'] = "Some thing went wrong."
		return Response(dictV)


	def delete(self, request):
		dictV = {}
		song_id = request.data.get('song_id')
		try:
			if song_id:
				song_obj = Song.objects.get(album__artist_id = request.user.id, delete = False, id = song_id)
				song_obj.delete = True
				song_obj.save()
				dictV['success'] = True
				dictV['data'] = "Song successfully deleted."
			else:
				dictV['success'] = False
				dictV['data'] = "Id is required."
		except Song.DoesNotExist:
			dictV['success'] = False
			dictV['data'] = "Song does not exist."

		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again."
		return Response(dictV)

"""
	All User's list.
					   """

class UserList(APIView):
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