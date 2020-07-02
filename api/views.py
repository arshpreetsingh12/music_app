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

class RegisterAPIView(APIView):
	authentication_classes = ()
	def post(self, request):
		context = {}

		data = {
			'first_name': request.data.get('first_name'),
			'username': request.data.get('username'),
			'password': request.data.get('password'),
			'email': request.data.get('email')
		}
		serializer = UserSerializer(data=data)
		if serializer.is_valid():

			user = serializer.save()
			print('user saved')
			if user:
				gender = request.data.get('gender')
				date_of_birth = request.data.get('date_of_birth')

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

				user_detail = UserDetail(
					user_id=user.id,
					gender=gender,
					date_of_birth=date_of_birth
					)
				user_detail.save()
				print(user_detail)
				context['success'] = True
				context['message'] = 'You signed up successfully'

		else:
			context['success'] = False
			context['error'] = 	serializer.errors				

		return Response(context)	

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
				context['message'] = 'Both fields are required'
				return Response(context)
			user = authenticate(username=username, password=password)
			print(user)
			if user:
				token, created = Token.objects.get_or_create(user=user)
				context['success'] = True
				if user.is_superuser or user.is_staff:
					context['is_superuser'] = True
				else:
					context['is_superuser']	= False
				context['message'] = 'Login Successful'
				context['data'] = {'token': token.key}
				user_data = {
					'username': user.username,
					'full_name': user.first_name,
					'email': user.email
				}
				context['user'] = user_data
				login(request, user)
			else:
				context['success'] = False
				context['message'] = 'Invalid credentials'
		except Exception as e:
			# raise euserserializser with update method
			context['success'] = False
			context['message'] = 'Something went wrong, Please try again'
		return Response(context)

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
			

class EditUserAPIView(APIView):
	permissions_classes = [IsAuthenticated]
	def put(self, request):
		context = {}

		if not request.data:
			context['success'] = False	
			context['message'] = 'Please enter detail you want to change' 
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
				context['message'] = 'Detail changed' 
			else:
				context['success'] = False	
				context['error'] = serializer.errors 
		except Exception as e:
			context['success'] = False	
			context['message'] = str(e)
		return Response(context)				

class AddArtistAPIView(APIView): # add artist
	authentication_classes = ()
	def post(self, request):
		context = {}
		artist = request.data.get('artist_name')
		user_id = request.data.get('user_id')
		artist_pic = request.data.get('artist_pic')
		if artist and user_id:
			data = {
				'artist':artist,
				'user':user_id,
				"artist_pic":artist_pic
			}
			try:
				Artist.objects.get(user_id = user_id)
				context['success'] = False
				context['error'] = 'Artist already exist.'
				return Response(context)
			except Artist.DoesNotExist:
				pass
			try:
				serializer = ArtistSerializer(data = data)
				if serializer.is_valid():
					serializer.save()
					print(serializer)
					context['success'] = True
					context['message'] = 'Artist saved'	
				else:
					context['success'] = False
					context['error'] = serializer.errors	
			except Exception as e:
				context['success'] = False
				context['error'] = 'Something went wrong. Please try again.'
		else:
			context['success'] = False
			context['error'] = 'artist_name and user_id both field is required'
		return Response(context)	


# class EditUserAPIView(GenericAPIView, UpdateModelMixin):
# 	permissions_classes = [IsAuthenticated]
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer
# 	def put(self, request):
# 		context = {}
# 		# username = request.data.get('username')
# 		try:
# 			return self.partial_update(request.user, data=request.data)
# 			# print(request.user)
# 			# serializer = UserSerializer(request.user, data=request.data, partial=True)
# 			# serializer.is_valid(raise_exception=True)
# 			# serializer.save()
# 			# print(serializer)	
# 		except Exception as e:
# 			raise e
# 		return Response(context)				




class AddSongAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		genre_id = request.data.get('genre_id')
		album_id = request.data.get('album_id')
		song = request.data.get('song')
		print(genre_id,album_id,'=======================')
		category_id = request.data.get('category_id')
		if not genre_id or not album_id or not song:
			context['success'] = False
			context['message'] = 'Required fields are missing.'
			return Response(context)

		# if not genre_id:
		# 	context['success'] = False
		# 	context['message'] = 'genre_id is required.'
		# 	return Response(context)
	
		# if not album_id:
		# 	context['success'] = False
		# 	return Response(context)
		# 	context['message'] = 'album_id is required.'
		# 	return Response(context)	
		
		# if not song:
		# 	context['success'] = False
		# 	context['message'] = 'song is required.'
		# 	return Response(context)	

		try:
			data = {
				'user': request.user.id,
				'genre': genre_id,
				'song': song,
				'album': album_id,
				'category':category_id
			}
			serializer = SongSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				context['success'] = True
				context['message'] = 'Song added'
			else:
				context['success'] = False
				context['error'] = serializer.errors
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong. Please try again'
		return Response(context)	

### delete song #####
class DeleteSongView(APIView):
	permission_classes = [IsAuthenticated]
	def delete(self, request):
		data = request.data.get('id')
		try:
			if data:
			    obj = Song.objects.get(pk=data, delete=False)
			    obj.delete = True
			    obj.save()
			    status = True
			    message = 'Successfully deleted'
			else:
				status = False
				message = 'Id is required.'
		except Song.DoesNotExist:
		    status = True
		    message = 'Song does not exist or song already deleted'

		dictV = {}
		dictV['status'] = status
		dictV['message'] = message
		return Response(dictV)



class LikeArtistAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		artist_id= request.data.get('artist_id')
		if artist_id:
			try:
				LikeArtist.objects.get(artist = artist_id, user_id = request.user.id, like = True)
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
					context['message'] = 'Liked artist'
				else:
					context['success'] = False
					context['error'] = serializer.errors
			except Exception as e:
				context['success'] = False
				context['message'] = 'Something went wrong. Please try again'
		else:
			context['success'] = False
			context['message'] = 'Artist id is required.'
		return Response(context)

class LikedArtistListAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			qs = LikeArtist.objects.filter(user_id=user_id, like = True)
			if not qs:
				context['success'] = False
				context['data'] = "User don't have liked artists"		
				return Response(context)
			serializer = LikeArtistSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)	

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
				context['success'] = False
				context['data'] = "User don't have songs"		
				return Response(context)
			serializer = SongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
	
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)					


# viewer adding song
# class UserAddSongAPIView(APIView):
# 	permission_classes =  [IsAuthenticated]
# 	def post(self, request):
# 		context = {}
# 		song_id = request.data.get('song_id')
# 		data = {
# 			'user':request.user.id,
# 			'song': song_id
# 		}
# 		try:
# 			serializer = UserSongSerializer(data=data)
# 			if serializer.is_valid():
# 				serializer.save()
# 				context['success'] = True
# 				context['message'] = 'Song added'
# 			else:
# 				context['success'] = False
# 				context['error'] = serializer.errors
# 		except Exception as e:
# 			context['success'] = False
# 			context['message'] = 'Something went wrong. Please try again'
# 		return Response(context)

# list of viewer song
class UserSongListAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			qs = UserSong.objects.filter(user_id=user_id)
			if not qs:
				context['success'] = False
				context['data'] = "User don't have songs"		
				return Response(context)
			serializer = UserSongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)		

class LikeSongAPIView(APIView):
	permissions_classes = [IsAuthenticated]
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
					context['message'] = 'Song liked'
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

class AllLikedSongsAPIView(APIView):
	permissions_classes = [IsAuthenticated]
	def get(self, request):
		context = {}
		user_id = request.user.id
		try:
			qs = LikeSong.objects.filter(user_id=user_id, like = True)
			if not qs:
				context['success'] = False
				context['data'] = "User doesn't have liked songs"		
				return Response(context)
			serializer = LikeSongSerializer(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data		
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)

class GenreAPIView(APIView):
	authentication_classes = ()
	def post(self, request):
		context = {}
		genre_name = request.data.get('genre_name')
		try:
			if genre_name:
				data = {
					'genre':genre_name,
				}
				serializer = GenreSerializer(data=data)
				if serializer.is_valid():
					serializer.save()
					context['success'] = True
					context['message'] = 'Genre saved'
				else:
					context['success'] = False
					context['error'] = serializer.errors
			else:
				context['success'] = False
				context['error'] = "Genre name is required."
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)

class AddAlbumAPIView(APIView):
	authentication_classes = ()
	def post(self, request):
		context = {}
		artist_id = request.data.get('artist_id')
		album = request.data.get('album')
		album_pic = request.data.get('album_pic')

		try:
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
					context['message'] = 'Album saved'
				else:
					context['success'] = False
					context['error'] = serializer.errors
			else:
				context['success'] = False
				context['error'] = "Artist id and album field is required."
		except Exception as e:
			context['success'] = False
			context['message'] = 'Something went wrong'		
		return Response(context)

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
				context['message'] = 'Mail sent'
			else:
				context['success'] = False
				context['message'] = "Error in email sending"
		except User.DoesNotExist:
			context['success'] = False
			context['message'] = "Email doesn't exist"	
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)



def mailSend(subject, recipient_list, message="", html_message=""):
	try:
		email_from = settings.EMAIL_HOST_USER
		print(html_message)
		send_mail( subject, message, email_from, recipient_list, html_message=html_message )
		print('------mail sent------')
		return True
	except Exception as e:
		print('-------error mail sending-------')
		return False	

class HideSongAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		song_id = request.data.get('song_id')
		hide = int(request.data.get('hide'))
		data = {
			'user':request.user.id,
			'song': song_id,
			'hide': hide
		}

		try:
			serializer = HideSongSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				context['success'] = True
				context['message'] = 'Song is hidden now'
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

class HiddenSongsListAPIView(APIView):
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

class CreatePlaylistAPIView(APIView):
	permission_classes = [IsAuthenticated]
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
					context['message'] = 'Playlist created'
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

class PlaylistTrackAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		playlist_id = request.data.get('playlist_id')
		song_id = request.data.get('song_id')
		
		if not playlist_id or not song_id:
			context['success'] = False
			context['message'] = "playlist_id and song_id both are required field."
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
				context['message'] = 'Song added to playlist'
			else:
				context['success'] = False
				context['error'] = serializer.errors	
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)

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
				context['success'] = False
				context['message'] = "Playlist doesn't exist"	
				return Response(context)

			serializer = PlaylistTrackSerializser(qs, many=True)
			context['success'] = True
			context['data'] = serializer.data
		except Exception as e:
			context['success'] = False
			context['message'] = "Something went wrong, Please try again"	
		return Response(context)	

########## for logged in artist user ############

class ArtistSongList(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		dictV = {}
		try:
			songs = Song.objects.filter(album__artist__user_id = request.user.id, delete = False)
			if songs:
				serializer = SongSerializer(songs, many=True)
				dictV['success'] = True
				dictV['data'] = serializer.data
			else:
				dictV['success'] = True
				dictV['data'] = 'This artist have no songs.'
		except Exception as e:
			dictV['success'] = False
			dictV['data'] = "Some thing went wrong."
		return Response(dictV)


class DeleteArtistSong(APIView):
	permission_classes = [IsAuthenticated]
	def delete(self, request):
		dictV = {}
		song_id = request.data.get('song_id')
		try:
			if song_id:
				song_obj = Song.objects.get(album__artist__user_id = request.user.id, delete = False, id = song_id)
				song_obj.delete = True
				song_obj.save()
				dictV['success'] = True
				dictV['data'] = "Your song has been successfully deleted."
			else:
				dictV['success'] = False
				dictV['data'] = "Id is required."
		except Song.DoesNotExist:
			dictV['success'] = False
			dictV['data'] = "Song does not exist or already deleted."

		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again"
		return Response(dictV)


class ArtistList(APIView):
	authentication_classes = ()
	def get(self, request):
		dictV = {}
		try:
			all_artist = Artist.objects.all()
			if all_artist:
				serializer = ArtistSerializer(all_artist, many=True)
				dictV['success'] = True
				dictV['data'] = serializer.data
			else:
				dictV['success'] = True
				dictV['data'] = 'No artist'
		except Exception as e:
			dictV['success'] = False
			dictV['data'] = "Some thing went wrong."
		return Response(dictV)

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
				dictV['data'] = 'No users'
		except Exception as e:
			dictV['success'] = False
			dictV['data'] = "Some thing went wrong."
		return Response(dictV)


################### For normal user  ##########################


class FollowUser(APIView):
	permission_classes = [IsAuthenticated]
	def post(self,request):
		dictV = {}
		following_user_id = request.data.get('id')
		if not following_user_id:
			dictV['success'] = False
			dictV['message'] = "Id field is required."
			return Response(dictV)	
	
		if following_user_id == request.user.id:
			dictV['success'] = False
			dictV['message'] = "Please enter that user id which you want follow."
			return Response(dictV)

		try:
			follwers = Follwer.objects.get(follower_user_id = request.user.id, following_user = following_user_id, is_follwed = True)
			dictV['success'] = False
			dictV['message'] = "You already follow this user"
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


# Logged in user's follower list
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
				dictV['data'] = 'No followers'
		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again"	
		return Response(dictV)


# Logged in user's following list
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
				dictV['data'] = 'No following.'
		except Exception as e:
			dictV['success'] = False
			dictV['message'] = "Something went wrong, Please try again"	
		return Response(dictV)