from django.contrib import admin

from .models import *


admin.site.register(UserDetail)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(LikeSong)
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(HideSong)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(LikeArtist)
admin.site.register(Category)
admin.site.register(Follwer)
