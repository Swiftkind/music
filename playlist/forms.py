from django import forms

from playlist.models import Playlist, Song


class PlaylistForm(forms.ModelForm):
    """To Add/Edit Playlist
    """

    class Meta:
        model = Playlist
        fields = ['title','description']


class SongForm(forms.ModelForm):
    """To Add/Edit Songs on playlist
    """

    class Meta:
        model = Song
        fields = ['title','link']