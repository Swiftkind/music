from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from playlist.models import Playlist, Song
from users.models import User
from playlist.forms import SongForm, PlaylistForm


class PlaylistsView(TemplateView):
    """Displays all playlist and can create playlist
    """
    template_name = 'playlist/playlists.html'

    def get(self, *args, **kwargs):
        """show all playlists
        """
        return render(self.request, self.template_name, {
            'playlists': Playlist.objects.all(),
        })

    def post(self, *args, **kwargs):
        """create playlist
        """
        form = PlaylistForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('playlists')
        return render(self.request, self.template_name, {
            'playlists': Playlist.objects.all(),
            'form': form,
        })


class PlaylistView(TemplateView):
    """Display a playlist and can add a song on that playlist
    """
    template_name = 'playlist/playlist.html'

    def get(self, *args, **kwargs):
        """show all songs from playlist
        """
        playlist = get_object_or_404(Playlist, id=kwargs['playlist_id'])
        songs = Song.objects.filter(playlist=playlist)
        return render(self.request, self.template_name, {
            'playlist': playlist,
            'songs': songs,
        })

    def post(self,*args,**kwargs):
        """add song to playlist
        """
        playlist = get_object_or_404(Playlist, id=kwargs['playlist_id'])
        songs = Song.objects.filter(playlist=playlist)
        form = SongForm(
            self.request.POST,
            user=self.request.user,
            playlist=playlist
        )
        if form.is_valid():
            form.save()
            return redirect('playlist', playlist.id)
        return render(self.request, self.template_name, {
            'playlist': playlist,
            'form': form,
            'songs': songs,
        })


class SongDetail(TemplateView):
    """ Display song details and can edit song from a playlist
    """
    template_name = 'playlist/detail.html'

    def get(self, *args, **kwargs): 
        """show song details
        """
        song = get_object_or_404(
            Song,
            id=kwargs['song_id'],
            user=self.request.user,
        )
        form = SongForm(instance=song)
        return render(self.request, self.template_name, {
                'form': form,
                'song': song,
        })

    def post(self, *args, **kwargs):
        """update song details
        """
        song = get_object_or_404(
            Song,
            id=kwargs['song_id'],
            user=self.request.user
        )
        form = SongForm(self.request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('playlist', kwargs['playlist_id'])
        return render(self.request, self.template_name, {
            'form': form,
        })


class SongDelete(View):
    """Delete Song from Playlist
    """

    def get(self, *args, **kwargs):
        song = get_object_or_404(Song,id=kwargs['song_id'])
        if self.request.user == song.user:
            song.delete()
            return redirect('playlist', kwargs['playlist_id'])
        raise Http404("User does not have permission to delete the song.")