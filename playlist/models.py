from django.db import models

from users.models import User


class Playlist(models.Model):
    """Playlist
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)


class Song(models.Model):
    """Song
    """
    playlist = models.ForeignKey(Playlist)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)