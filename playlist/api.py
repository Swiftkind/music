from playlist.models import Playlist
from playlist.serializers import PlaylistSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from rest_framework import status
from .models import Playlist


class PlaylistViewSet(viewsets.ViewSet):
    """ Playlist functions
    """
    def add_playlist(self, request):
        serializer = PlaylistSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete_playlist(self, request, playlist_id):
        instance = get_object_or_404(Playlist, pk=playlist_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
