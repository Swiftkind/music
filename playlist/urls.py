from django.conf.urls import url

from playlist import views

urlpatterns = [
url(r'^$', views.PlaylistView.as_view(), name='playlists'),
url(r'^(?P<playlist_id>\d+)/$',views.PlaylistDetail.as_view(),name='playlist_detail'),
url(r'^(?P<playlist_id>\d+)/delete/$',views.PlaylistDelete.as_view(),name='playlist_delete'),
url(r'^(?P<playlist_id>\d+)/songs/$',views.PlaylistSongs.as_view(),name='playlist_songs'),
url(r'^(?P<playlist_id>\d+)/songs/(?P<song_id>\d+)/$',views.SongDetail.as_view(),name='playlist_songdetail'),
url(r'^(?P<playlist_id>\d+)/songs/(?P<song_id>\d+)/delete/$',views.SongDelete.as_view(),name='playlist_songdelete'),
]

