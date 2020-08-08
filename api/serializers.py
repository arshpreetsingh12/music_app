from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import *

class UserSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(required=True) # full name
	username = serializers.CharField(
			required=True, 
			validators = [UniqueValidator(queryset=User.objects.all())]
			)
	email = serializers.CharField(
			required=True, 
			validators = [UniqueValidator(queryset=User.objects.all())] 
			)
	password = serializers.CharField(min_length=8,required=True)
	

	def validate(self, data):
		password = data.get('password')

		try:
			validate_password(password=password)
		except Exception as e:
			pass
		return super(UserSerializer, self).validate(data)
		
	def create(self, validated_data):
		user = User.objects.create_user(
			first_name=validated_data['first_name'],
			username=validated_data['username'],
			email=validated_data['email'],
			password=validated_data['password'],
			)
		user.save()
		return user
	

	class Meta:
		model = User
		fields = (
			'first_name',
			'username',
			'email',
			'password',
			)


class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDetail
		fields = ['user','is_artist','is_listener','profile_pic']

class ArtistInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtistInfo
		fields = ['info','genre','country','website','company_label']


class ArtistSocialData(serializers.ModelSerializer):
	class Meta:
		model = SocialMedia
		fields = ['id','user_info','link_type','link']

		

class AllArtistDataSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()

	class Meta:
		model = ArtistInfo
		fields = ['id', 'name', 'image']

	def get_name(self, instance):
		return instance.info.user.first_name

	def get_image(self, instance):
		return instance.info.profile_pic.url

# class ArtistSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Artist
# 		fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
	class Meta:
		model = Song
		fields = ['id','user','genre','song_title','song_length','song_image','song_mp3','description']	


class LikeArtistSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()

	class Meta:
		model = ArtistInfo
		fields = ['id', 'name', 'image']

	def get_name(self, instance):
		return instance.artist.info.user.first_name

	def get_image(self, instance):
		return instance.artist.info.profile_pic.url


class HiddenArtistSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()

	class Meta:
		model = ArtistInfo
		fields = ['id', 'name', 'image']

	def get_name(self, instance):
		return instance.artist.info.user.first_name

	def get_image(self, instance):
		return instance.artist.info.profile_pic.url


class LikeSongSerializer(serializers.ModelSerializer):
	class Meta:
		model = LikeSong	
		fields = '__all__'	

class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre	
		fields = ["id","genre","genre_color","color_hexcode"]

class AlbumSerializer(serializers.ModelSerializer):
	class Meta:
		model = Album	
		fields = ['id','artist','song','album','album_pic','album_length','description']

class HideSongSerializer(serializers.ModelSerializer):
	class Meta:
		model = HideSong	
		fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Playlist	
		fields = ['id','user','playlist','cover_image']

class AddPlaylistTrack(serializers.ModelSerializer):
	
	class Meta:
		model = PlaylistTrack
		fields = '__all__'

class PlaylistTrackSerializser(serializers.ModelSerializer):	
	artist_name = serializers.SerializerMethodField()
	song_title = serializers.SerializerMethodField()
	song_length = serializers.SerializerMethodField()
	song_image = serializers.SerializerMethodField()
	song_mp3 = serializers.SerializerMethodField()

	class Meta:
		model = Song
		fields = ['id','artist_name', 'song_title', 'song_length','song_image','song_mp3']

	def get_artist_name(self, instance):
		return instance.song.user.user.first_name

	def get_song_title(self, instance):
		return instance.song.song_title

	def get_song_length(self, instance):
		return instance.song.song_length

	def get_song_image(self, instance):
		if instance.song.song_image:
			return instance.song.song_image.url
		else:
			return '/media/noimage.jpg'

	def get_song_mp3(self, instance):
		return instance.song.song_mp3.url


class FollowUserSerializser(serializers.ModelSerializer):
	
	class Meta:
		model = Follwer
		fields = ['follower_user','following_user','is_follwed']		

class CountrySerializser(serializers.ModelSerializer):
	
	class Meta:
		model = Country
		fields = '__all__'		


# class AlbumSongsSerializser(serializers.ModelSerializer):
	
# 	class Meta:
# 		model = AlbumSongs
# 		fields = '__all__'		


class ForgetPasswordSerializser(serializers.ModelSerializer):
	
	class Meta:
		model = ForgetPassword
		fields = '__all__'		




