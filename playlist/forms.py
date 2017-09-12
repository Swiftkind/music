from django import forms
from playlist.models import Playlist,Song 

class PlaylistForm(forms.ModelForm):
    """
    Form for Adding and Editing Playlist
    """
    class Meta:
        model = Playlist
        fields = ['title','description']

class SongListForm(forms.ModelForm):
    """
    Form for Adding and Editing Song
    """
    class Meta:
        model = Song
        fields = ['title','link']

    def save(self,*args,**kwargs):
        #overwritten so that song saves to playlist
        title = self.data.get('title')
        link = self.data.get('link')
        add_song = kwargs.get('playlist_id')

        #to save new song to playlist
        if add_song:
            song = Song.objects.create(title = title,link = link)
            pl = Playlist.objects.get(id = add_song)
            pl.songs.add(song)
            #so that it can be used for ajax
            self.song = song
            self.playlist_id = kwargs['playlist_id']

        #condition when to edit Song
        else:
            song = Song.objects.filter(id = self.instance.id)
            song.update(title = title,link = link)
        return