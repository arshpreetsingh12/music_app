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
	is_listener = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.first_name


class Country(models.Model):
	country_code = models.CharField(max_length=50, null = True, blank = True)
	country_name = models.CharField(max_length=50, null = True, blank = True)

	def __str__(self):
		return self.country_code


""" Admin can add Genre for songs """
class Genre(models.Model):
	genre = models.CharField(max_length=50)
	genre_color = models.CharField(max_length=50,null = True, blank = True)
	color_hexcode = models.CharField(max_length=50,null = True, blank = True)

	def __str__(self):
		return self.genre


""" This table for artist's extra details. """
class ArtistInfo(models.Model):
	info = models.OneToOneField(UserDetail, on_delete=models.CASCADE)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null = True, blank = True)
	website = models.CharField(max_length=250)
	company_label = models.CharField(max_length=500)
	social_media = models.CharField(max_length=500)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.info.user.first_name

		
""" When uploader upload any song that object saved in this table """
class Song(models.Model):
	user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True)
	genre = models.ForeignKey(Genre, blank=True, null=True, on_delete=models.CASCADE)	
	song_title = models.CharField(max_length=50, null = True, blank = True)
	song_length = models.CharField(max_length=50, null = True, blank = True)
	song_image = models.FileField(upload_to = "song_image", null = True, blank = True)
	song_mp3 = models.FileField(upload_to = "song_mp3", null = True, blank = True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	delete = models.BooleanField(default = False)
	description = models.TextField(max_length=1000, null = True, blank = True)


""" When uploader upload any album that object saved in this table  """
class Album(models.Model):
	artist = models.ForeignKey(UserDetail, blank=True, null=True, on_delete=models.CASCADE)
	song = models.ManyToManyField(Song)
	album = models.CharField(max_length=50)
	album_pic = models.ImageField(blank=True, null=True)
	album_length = models.CharField(max_length=50, null = True, blank = True)
	fb_url = models.URLField(max_length=500, null = True, blank = True)
	twitter_url = models.URLField(max_length=500, null = True, blank = True)
	google_url = models.URLField(max_length=500, null = True, blank = True)
	website_url = models.URLField(max_length=500, null = True, blank = True)
	description = models.TextField(max_length=1000, null = True, blank = True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.album

""" When uploader upload any album that object saved in this table  """
# class AlbumSongs(models.Model):
# 	albums = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE)
# 	song = models.ForeignKey(Song, blank=True, null=True, on_delete=models.CASCADE)

	# def __str__(self):
	# 	return self.albums.album


""" When user like any artist that object saved in this table """
class LikeArtist(models.Model):
	user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
	artist = models.ForeignKey(User, related_name='artist', null= True, blank = True, on_delete=models.CASCADE)
	like = models.BooleanField(default=False)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.first_name

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
	artist = models.ForeignKey(ArtistInfo, on_delete=models.CASCADE, null = True, blank = True)
	playlist = models.CharField(max_length=50)
	cover_image = models.FileField(upload_to = 'play_list', null = True, blank = True)
	description = models.TextField(max_length=1000, null = True, blank = True)
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


class ForgetPassword(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
	activation_key = models.CharField(max_length=100, verbose_name='Activation Key')
	created_at  = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.first_name 