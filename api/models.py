from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
    ('NB', 'Non-Binary') 
	) 


""" This table for user's extra details. """
class UserDetail(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
	is_artist = models.BooleanField(default=False)
	is_normal = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.first_name


""" When uploader upload any album that object saved in this table  """
class Album(models.Model):
	artist = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	album = models.CharField(max_length=50)
	album_pic = models.ImageField(blank=True, null=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.album

""" Admin can add Genre for songs """
class Genre(models.Model):
	genre = models.CharField(max_length=50)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.genre

""" When uploader upload any song that object saved in this table """
class Song(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	genre = models.ForeignKey(Genre, blank=True, null=True, on_delete=models.CASCADE)	
	album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE)
	song = models.FileField(upload_to = "song")
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	delete = models.BooleanField(default = False)

""" When user like any artist that object saved in this table """
class LikeArtist(models.Model):
	user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
	artist = models.ForeignKey(User, related_name='artist', null= True, blank = True, on_delete=models.CASCADE)
	like = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.artist.artist

""" When user like any song that object saved in this table """
class LikeSong(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, on_delete=models.CASCADE)
	like = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


""" When user hide any song that object saved in this table """
class HideSong(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, on_delete=models.CASCADE)
	hide = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


""" When user create their playlist that object saved in this table """
class Playlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	playlist = models.CharField(max_length=50)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.playlist


""" When user add song in their playlist that object saved in this table """
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

	def __str__(self):
		return self.follower_user.first_name