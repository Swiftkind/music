from django import forms

from playlist.models import Song, Playlist


class PlaylistForm(forms.ModelForm):
    """To Add/Edit Playlist
    """

    class Meta:
        model = Playlist
        fields = ['title', 'description']


class SongForm(forms.ModelForm):
    """To Add/Edit Song
    """

    class Meta:
        model = Song
        fields = ['title', 'link']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.playlist = kwargs.pop('playlist', None)
        return super(SongForm, self).__init__(*args, **kwargs)

    def save(self):
        instance = super(SongForm, self).save(commit=False)
        if self.user is not None and self.playlist is not None:
            instance.user = self.user
            instance.playlist = self.playlist
        instance.save()
        return instance
