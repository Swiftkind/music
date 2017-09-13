from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse


from playlist.models import Playlist, Song
from playlist.forms import PlaylistForm, SongForm


class PlaylistsView(TemplateView):
    """List Playlists and Create Playlist
    """
    template_name = "playlist/playlists.html"
    form = PlaylistForm

    def get(self, *args, **kwargs):
        playlists = Playlist.objects.all().order_by('-date_created')
        context = {'playlists':playlists,
                   'form':self.form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            form.save()
            view_url = reverse('playlist', args=(form.instance.id,))
            edit_url = reverse('playlist_detail', args=(form.instance.id,))
            delete_url = reverse('delete_playlist', args=(form.instance.id,))
            context = {'id':form.instance.id, 'title':form.instance.title,
                       'view_url':view_url, 'edit_url':edit_url,
                       'delete_url':delete_url}
            return JsonResponse(context,safe=False)
        else:
            return JsonResponse({'form': form.errors['title']},safe=False)


class PlaylistView(TemplateView):
    """ View Playlist
    """
    template_name = "playlist/playlist.html"

    def get(self, *args, **kwargs):
        playlist_id = kwargs['playlist_id']
        playlist = Playlist.objects.get(id=playlist_id)
        context = {'playlist':playlist}
        return render(self.request, self.template_name, context)


class PlaylistDetail(TemplateView):
    """ Playlist Detail to edit and Edit Playlist Info
    """
    template_name = "playlist/playlist_detail.html"
    form = PlaylistForm

    def get(self, *args, **kwargs):
        playlist_id = kwargs['playlist_id']
        playlist = Playlist.objects.get(id=playlist_id)
        form = self.form(instance = playlist)
        context = {'form':form, 'playlist':playlist}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        playlist_id = kwargs['playlist_id']
        playlist = Playlist.objects.get(id=playlist_id)
        form = self.form(self.request.POST, instance = playlist)
        if form.is_valid():
            form.save()
            return redirect('playlists')
        return render(self.request, self.template_name, {'form':form})


class PlaylistDelete(View):

        def get(self, *args, **kwargs):
            playlist_id = kwargs['playlist_id']
            playlist = Playlist.objects.get(id=playlist_id)
            Playlist.objects.get(id= playlist_id).delete()
            return redirect('playlists')