import re

from django import forms

from playlist.models import Song, Playlist
from playlist.YoutubeApi import Youtube

class PlaylistForm(forms.ModelForm):
    """Form for creating playlist
    """

    class Meta:
        model = Playlist
        fields = ['title', 'description']
        unique_together = ('title','user')

    def __init__(self, *args, **kwargs):
        """ playlist needs an owner
        """
        self.user = kwargs.pop('user', None)
        return super(PlaylistForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """ overridden save
        """
        instance = super(PlaylistForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance


    def clean_title(self):
        """ overriden so that there cannot be the same playlist name from a user
        """
        playlist = Playlist.objects.filter(
            title=self.cleaned_data['title'],
            user=self.user
        )

        if playlist.exists():
            raise forms.ValidationError(
                'You already have a playlist with the same name'
            )
        
        return self.cleaned_data['title']


class SongForm(Youtube, forms.ModelForm):
    """Form for adding song on a playlist
    """
    link = forms.CharField(max_length=60)

    class Meta:
        model = Song
        fields = ['link']

    def __init__(self, *args, **kwargs):
        """ User and playlist are used for creation of song
        """
        self.user = kwargs.pop('user', None)
        self.playlist = kwargs.pop('playlist', None)

        return super(SongForm, self).__init__(*args, **kwargs)

    def clean_link(self):
        """ check link validations
        """
        yt_code = self.cleaned_data['link']
        #check youtube id length validation
        if len(yt_code) < 11:
            raise forms.ValidationError("Youtube id length is invalid.")
        elif len(yt_code) > 11:
            #turns full url into proper youtube id needed
            yt_id = re.search(
                '((?<=/v/)\S+|(?<=v=)\S+|(?<=be/)\S+|(?<=/embed/)\S+)',
                yt_code
            )
            #gets the youtube id after the delimter
            yt_code = yt_id.group()[:11]
        #check if song already exists
        song = Song.objects.filter(
            link=yt_code,
            user=self.user,
            playlist=self.playlist,
            archive=False
            )
        if song.exists():
            raise forms.ValidationError("Song already exists on this playlist.")
     
        # Validates if the user added recently a song 
        all_song = Song.objects.filter(archive=False, playlist=self.playlist)
        if all_song.exists():
            get_last_user = all_song.last().user
            if self.user == get_last_user:
                raise forms.ValidationError('You cannot add right now!')

        return yt_code

    def save(self, commit=True):
        """ Song creation needs user and playlist 
        """
        song = super(SongForm, self).save(commit=False)
        # if self.user and self.playlist exists then it creates otherwise update
        song.user = self.user if self.user else self.instance.user
        song.playlist = self.playlist if self.playlist else self.instance.playlist
        yt_video = self.set_data(song.link)
        song.title = self.get_title()
        song.thumb_url = self.get_image_url()
        song.duration = self.get_duration(self.get_time_code())
        song.save()
        return song


class SearchPlaylist(forms.Form):
    keyword = forms.CharField()