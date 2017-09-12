from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View

from playlist.models import Song, Playlist
from playlist.forms import PlaylistForm, SongListForm


class PlaylistView(TemplateView):
    """
    Display Index
    """
    template_name = "playlist/playlists.html"

    def get(self,*args,**kwargs):
        #Display the Playlists
        form= PlaylistForm()
        pl = Playlist.objects.all().order_by('-date_created')
        #import pdb; pdb.set_trace()
        context = {'form':form,
                    'pl':pl}
        return render(self.request,self.template_name,context)

    def post(self,*args,**kwargs):
        #create new playlist
        form = PlaylistForm(self.request.POST)
        form.save()
        return JsonResponse({'id':form.instance.id, 'title': form.instance.title , 'description':form.instance.description},safe = False)


class PlaylistDetail(TemplateView):
    """
    View Playlist Detail
    """
    template_name = "playlist/playlist_detail.html"

    def get(self,*args,**kwargs):
    #View Playlist Details for Edit
        playlist = Playlist.objects.get(id= kwargs['playlist_id'])
        form = PlaylistForm()
        context = {'form':form,'playlist':playlist}
        return render(self.request,self.template_name,context)

    def post(self,*args,**kwargs):
    # to edit playlist details
        playlist = Playlist.objects.get(id= kwargs['playlist_id'])
        form = PlaylistForm(self.request.POST,instance = playlist)
        form.save()
        return redirect('playlists')


class PlaylistDelete(View):

        def post(self,*args,**kwargs):
        # to delete playlist details

        #insert user restrictions here later
            Playlist.objects.get(id= kwargs['playlist_id']).delete()
            return redirect('playlists')


class PlaylistSongs(TemplateView):
    """
    View songs from a Playlist
    """
    template_name = "playlist/playlist_songs.html"

    def get(self,*args,**kwargs):
        # show songs in the playlist
        playlist = Playlist.objects.get(id= kwargs['playlist_id'])
        form = SongListForm()
        songlist = playlist.songs.all().order_by('date_created')
        context = {'form':form,'playlist':playlist,'songlist':songlist}
        return render(self.request,self.template_name,context)

    def post(self,*args,**kwargs):
        #add song to playlist
        form = SongListForm(self.request.POST)
        form.save(playlist_id = kwargs['playlist_id'])
        return JsonResponse({'id':form.song.id, 'title': form.data['title'] , 'link':form.data['link'],'playlist_id':form.playlist_id},safe = False)


class SongDetail(TemplateView):
    """
    View Song Detail from a specific Playlist
    """
    template_name = "playlist/song_detail.html"

    def get(self,*args,**kwargs):
        #display song detail
        playlist = Playlist.objects.get(id= kwargs['playlist_id'])
        song = Song.objects.get(id = kwargs['song_id'])
        form = SongListForm()
        context = {'form':form, 'song':song, 'playlist':playlist,
                   'playlist_id':kwargs['playlist_id']}
        return render(self.request, self.template_name, context)

    def post(self,*args,**kwargs):
        # edit song detail
        song = Song.objects.get(id = kwargs['song_id'])
        form = SongListForm(self.request.POST,instance = song)
        form.save()
        return redirect('playlist_songs',playlist_id=kwargs['playlist_id'])


class SongDelete(View):
    """
    Delete Song From List
    """
    def post(self,request, *args, **kwargs):
        #import pdb;pdb.set_trace()
        Song.objects.get(id = kwargs['song_id']).delete()
        return redirect('playlist_songs',playlist_id=kwargs['playlist_id'])