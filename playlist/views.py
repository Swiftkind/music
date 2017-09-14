from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from playlist.models import Playlist, Song
from users.models import User
from playlist.forms import SongForm


class PlaylistView(TemplateView):
    """ViewPlaylist && Add song
    """
    template_name = 'playlist/playlist.html'
    form = SongForm

    def get(self,*args,**kwargs):
        playlist = get_object_or_404(Playlist, id=kwargs['playlist_id'])
        songs = Song.objects.filter(playlist=playlist)
        context={
            'playlist':playlist,
            'form':self.form,
            'songs':songs,}
        return render(self.request, self.template_name, context)

    def post(self,*args,**kwargs):
        playlist = get_object_or_404(Playlist, id=kwargs['playlist_id'])
        songs = Song.objects.filter(playlist=playlist)
        form = self.form(self.request.POST)
        if form.is_valid:
            form.instance.playlist = playlist
            form.instance.user = self.request.user
            form.save()
            return redirect('playlist',kwargs['playlist_id'])
        context={
            'playlist':playlist,
            'form':form,
            'songs':songs}
        return render(self.request,template_name,context)

