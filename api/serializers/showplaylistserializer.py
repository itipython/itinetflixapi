from rest_framework import serializers
from netflixdb.models import ShowPlaylist

class ShowPlaylistSerializer(serializers.ModelSerializer):
    showposter = serializers.ReadOnlyField(source='show.posterURL')
    showname = serializers.ReadOnlyField(source='show.name')


    class Meta:
        model = ShowPlaylist
        exclude = ['id','user']
        order_by = ['showname']
