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
		print(user)
		return user

	
		

	class Meta:
		model = User
		fields = (
			'first_name',
			'username',
			'email',
			'password',
			)

# class ProfileSerializer(serializers.ModelSerializer):
# 	gender = serializers.CharField(source='get_gender_display', required=True)
# 	date_of_birth = serializers.DateField(format="%Y-%m-%d", required=True)

# 	print(gender)
# 	print(date_of_birth)
# 	def create(self, validated_data):
		
# 		user = self.context['user']
# 		print(f"user: {user}")
# 		gender = validated_data['gender']
# 		date_of_birth = validated_data['date_of_birth']

# 		profile = Profile(
# 			user=user,
# 			gender=gender,
# 			date_of_birth=date_of_birth
# 			)
# 		profile.save()
# 		print(profile)
# 		return profile	

# 	class Meta:
# 		model = Profile	
# 		fields = ('user', 'gender', 'date_of_birth')


class ArtistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Artist
		fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
	class Meta:
		model = Song
		fields = '__all__'	

# class UserSongSerializer(serializers.ModelSerializer):
# 	song = SongSerializer()
# 	class Meta:
# 		model = UserSong
# 		fields = '__all__'

class LikeArtistSerializer(serializers.ModelSerializer):
	class Meta:
		model = LikeArtist
		fields = '__all__'			

class LikeSongSerializer(serializers.ModelSerializer):
	# song = SongSerializer()
	class Meta:
		model = LikeSong	
		fields = '__all__'	

class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre	
		fields = '__all__'	

class AlbumSerializer(serializers.ModelSerializer):
	# artist = ArtistSerializer()
	class Meta:
		model = Album	
		fields = '__all__'

class HideSongSerializer(serializers.ModelSerializer):
	# song = SongSerializer()
	class Meta:
		model = HideSong	
		fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Playlist	
		fields = '__all__'

class PlaylistTrackSerializser(serializers.ModelSerializer):
	# song = SongSerializer(many=True)
	# playlist= PlaylistSerializer(many=True)
	
	class Meta:
		model = PlaylistTrack
		fields = '__all__'		


class FollowUserSerializser(serializers.ModelSerializer):
	
	class Meta:
		model = Follwer
		fields = '__all__'		

