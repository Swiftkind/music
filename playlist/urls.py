from django.conf.urls import url

from .views import PlaylistsView, PlaylistView, SongDetail, SongDelete

urlpatterns = [
    url(r'^$', PlaylistsView.as_view(), name ="playlists"),
    url(r'^playlist/(?P<playlist_id>\d+)/$', PlaylistView.as_view(), name ="playlist"),
    url(r'^playlist/(?P<playlist_id>\d+)/(?P<song_id>\d+)/$', SongDetail.as_view(), name ="song_detail"),
    url(r'^playlist/(?P<playlist_id>\d+)/(?P<song_id>\d+)/delete/$', SongDelete.as_view(), name ="song_delete"),
]
