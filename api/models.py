from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
    ('NB', 'Non-Binary') 
	) 


class UserDetail(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
	is_uploader = models.BooleanField(default=False)
	is_normal = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Artist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	artist = models.CharField(max_length=50)
	artist_pic = models.ImageField(upload_to = "artist",blank=True, null=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Album(models.Model):
	artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.CASCADE)
	album = models.CharField(max_length=50)
	album_pic = models.ImageField(blank=True, null=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Genre(models.Model):
	genre = models.CharField(max_length=50)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
	category_name = models.CharField(max_length=50)
	description = models.CharField(max_length=500)	
	image = models.ImageField(upload_to = "category", blank=True, null=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Song(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	genre = models.ForeignKey(Genre, blank=True, null=True, on_delete=models.CASCADE)	
	album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
	song = models.FileField(upload_to = "song")
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	delete = models.BooleanField(default = False)

# class UserSong(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	song = models.OneToOneField(Song, on_delete=models.CASCADE)
# 	created_at  = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)

class LikeArtist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	like = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class LikeSong(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, on_delete=models.CASCADE)
	like = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class HideSong(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, on_delete=models.CASCADE)
	hide = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Playlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	playlist = models.CharField(max_length=50)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class PlaylistTrack(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, on_delete=models.CASCADE)
	playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

"""
	This is Table for follwer and follwing both users. 
	follower_user : The user who follow following_user.
	following_user: The user whom follow follower_user.  

													"""
class Follwer(models.Model):
	follower_user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE,)
	following_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE,)	
	is_follwed = models.BooleanField(default = False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)