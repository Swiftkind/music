from rest_framework import serializers
from playlist.models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id','title','user_email','get_thumb_url',)

    def get_user_email(self, obj):
        return obj.user.email