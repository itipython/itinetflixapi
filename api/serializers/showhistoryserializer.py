from rest_framework import serializers
from netflixdb.models import ShowHistory

class ShowHistorySerializer(serializers.ModelSerializer):
    showposter = serializers.ReadOnlyField(source='show.posterURL')
    showname = serializers.ReadOnlyField(source='show.name')

    class Meta:
        model = ShowHistory
        exclude = ['id','user']
        order_by = ['watchDate']
