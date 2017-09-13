from django.db import models


class Playlist(models.Model):
    """Songlist
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    """Song
    """
    playlist = models.ForeignKey(Playlist)
    title = models.CharField(max_length=255)
    link = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link