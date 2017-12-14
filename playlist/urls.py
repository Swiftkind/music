
from django.conf.urls import url

from .views import (
    AllPlaylistView,
    PlaylistView,
    SongDetail,
    SongDelete,
    SearchSongYoutube,
    SearchedPlaylist,
    AddToPlaylistFromYoutube
    )

from playlist.api import(
    PlaylistViewSet,
    )

urlpatterns = [
    url(r'^$', AllPlaylistView.as_view(), name='all_playlist'),
    url(r'^playlist/(?P<playlist_id>\d+)/$', PlaylistView.as_view(), name='playlist'),
    url(r'^playlist/(?P<playlist_id>\d+)/(?P<song_id>\d+)/$', SongDetail.as_view(), name='song_detail'),
    url(r'^playlist/(?P<playlist_id>\d+)/(?P<song_id>\d+)/delete/$', SongDelete.as_view(), name='song_delete'),
    url(r'^playlist/search/$', SearchSongYoutube.as_view(), name='search_youtube'),
    url(r'^playlist/playlistsearch/$', SearchedPlaylist.as_view(), name='search_playlist'),
    url(r'^playlist/search/add/$', AddToPlaylistFromYoutube.as_view(), name='add_youtube_search'),
    # DRF API
    url(r'^api/playlist/$', PlaylistViewSet.as_view(
        {'post': 'add_playlist', 'delete': 'delete_playlist'}), name='playlist'),
    url(r'^api/playlist/delete/(?P<playlist_id>\d+)/$', PlaylistViewSet.as_view(
        {'post': 'delete_playlist'}), name='delete_playlist'),
    url(r'^api/playlist/update/(?P<playlist_id>\d+)/$', PlaylistViewSet.as_view(
        {'post': 'update_playlist'}), name='update_playlist'),
    ]